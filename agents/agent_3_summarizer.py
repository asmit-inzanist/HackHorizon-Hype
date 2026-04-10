"""
Agent 3 — Record Summarizer

Model: Gemini 1.5 Flash (accuracy critical)
Purpose:
  - Generates a clean patient summary for doctor view
  - Performs allergy cross-check against patient profile
  - Raises warnings if prescription contains allergens
  - Triggers TTS alert for allergy warnings via gTTS
"""

import json
import logging
from google import genai
from google.genai import types
from core.config import get_settings
from services.tts_service import synthesize_and_upload

logger = logging.getLogger(__name__)

SUMMARY_PROMPT = """You are a medical record summarizer creating a report for a doctor.

PATIENT PROFILE:
- Name: {patient_name}
- Age: {patient_age}
- Blood Group: {blood_group}
- Known Allergies: {allergies}
- Chronic Conditions: {chronic_conditions}

MEDICAL RECORDS (all past prescriptions and reports):
{records_json}

Generate a comprehensive patient summary and allergy cross-check.
Return ONLY valid JSON (no markdown, no code blocks):
{{
    "summary_text": "A clean, professional doctor-facing summary paragraph covering: patient overview, current medications, diagnosis history, important observations, and recommendations. Write in clear medical language.",
    "allergy_warnings": [
        {{
            "medicine": "name of the medicine that conflicts",
            "allergy": "the patient's allergy it conflicts with",
            "severity": "high/medium/low",
            "message": "Clear warning message explaining the risk"
        }}
    ],
    "key_observations": [
        "Important observation 1",
        "Important observation 2"
    ]
}}

CRITICAL RULES:
- Cross-check EVERY prescribed medicine against the patient's known allergies
- Check for drug interactions with chronic conditions
- If ANY medicine matches or is related to an allergy, add a warning with severity "high"
- If a medicine may exacerbate a chronic condition, add a warning with severity "medium"
- Be thorough — missing an allergy warning is a patient safety issue
- If no allergies or conflicts are found, return an empty allergy_warnings array
"""


def _get_client() -> genai.Client:
    """Create a Gemini client."""
    settings = get_settings()
    return genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_summary(
    patient_profile: dict,
    medical_records: list[dict],
    user_id: str,
) -> dict:
    """
    Generate a comprehensive patient summary with allergy cross-checking.

    Args:
        patient_profile: The patient's profile data (allergies, conditions, etc.)
        medical_records: List of all medical records with extracted_data.
        user_id: Patient's user ID (for TTS file storage).

    Returns:
        Dict with summary_text, allergy_warnings, and optional audio_url.
    """
    client = _get_client()

    # Build records summary for the prompt
    records_for_prompt = []
    for record in medical_records:
        entry = {
            "date": record.get("created_at", "unknown"),
            "type": record.get("file_type", "unknown"),
            "extracted": record.get("extracted_data", {}),
            "transcription": record.get("transcription"),
        }
        records_for_prompt.append(entry)

    prompt = SUMMARY_PROMPT.format(
        patient_name=patient_profile.get("full_name", "Unknown"),
        patient_age=patient_profile.get("age", "Unknown"),
        blood_group=patient_profile.get("blood_group", "Unknown"),
        allergies=", ".join(patient_profile.get("allergies", [])) or "None reported",
        chronic_conditions=", ".join(patient_profile.get("chronic_conditions", [])) or "None reported",
        records_json=json.dumps(records_for_prompt, indent=2, default=str),
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Low temperature for accuracy
                max_output_tokens=4096,
            ),
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        result = json.loads(raw_text)

        summary_text = result.get("summary_text", "")
        allergy_warnings = result.get("allergy_warnings", [])

        logger.info(
            f"Agent 3: Summary generated — "
            f"{len(allergy_warnings)} allergy warnings found"
        )

        # ── Generate TTS audio for allergy warnings ──
        audio_url = None
        if allergy_warnings:
            # Build a spoken warning message
            warning_texts = []
            warning_texts.append("ALLERGY ALERT. The following warnings were detected:")
            for w in allergy_warnings:
                warning_texts.append(
                    f"Warning: {w['medicine']} may conflict with your "
                    f"known allergy to {w['allergy']}. "
                    f"Severity: {w['severity']}. {w['message']}"
                )
            warning_texts.append(
                "Please consult your doctor immediately before taking these medications."
            )

            full_warning_text = " ".join(warning_texts)

            try:
                audio_url = await synthesize_and_upload(
                    text=full_warning_text,
                    language="en",
                    user_id=user_id,
                )
                logger.info(f"Agent 3: Allergy warning TTS generated: {audio_url}")
            except Exception as e:
                logger.error(f"Agent 3: TTS generation failed: {e}")

        return {
            "summary_text": summary_text,
            "allergy_warnings": allergy_warnings,
            "audio_url": audio_url,
            "key_observations": result.get("key_observations", []),
        }

    except json.JSONDecodeError as e:
        logger.error(f"Agent 3: Failed to parse summary JSON: {e}")
        return {
            "summary_text": "Failed to generate summary. Please try again.",
            "allergy_warnings": [],
            "audio_url": None,
        }
    except Exception as e:
        logger.error(f"Agent 3: Summary generation error: {e}")
        raise
