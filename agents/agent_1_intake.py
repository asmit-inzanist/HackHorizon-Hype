"""
Agent 1 — Document Intake

Model: Gemini 1.5 Flash (Vision)
Purpose:
  - Reads uploaded prescriptions / medical reports (images or PDFs)
  - Extracts medicines, dosage, frequency, diagnosis, doctor name, hospital, date
  - Merges voice note transcription if provided
  - Returns structured JSON
"""

import json
import base64
import logging
from google import genai
from google.genai import types
from core.config import get_settings

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a medical document analysis AI. Analyze the provided medical document 
(prescription, lab report, or imaging report) and extract the following information into a structured JSON format.

IMPORTANT: Return ONLY valid JSON, no markdown formatting, no code blocks, no extra text.

Required JSON structure:
{
    "medicines": [
        {
            "name": "medicine name",
            "dosage": "dosage amount (e.g., 500mg)",
            "frequency": "how often (e.g., twice daily)",
            "duration": "for how long (e.g., 7 days)"
        }
    ],
    "diagnosis": "primary diagnosis or condition",
    "doctor_name": "name of the prescribing doctor",
    "hospital": "hospital or clinic name",
    "date": "date of the document (YYYY-MM-DD if possible)",
    "notes": "any additional relevant notes or observations"
}

Rules:
- Extract ALL medicines listed in the document
- If a field is not visible or not applicable, set it to null
- For handwritten prescriptions, do your best to read the medicine names
- Be precise with dosage and frequency
- If the document is a lab report, list any medications mentioned and include test results in notes
"""

MERGE_PROMPT = """You are merging data from two sources about the same medical visit:

1. DOCUMENT EXTRACTION (from a scanned prescription/report):
{doc_data}

2. VOICE NOTE TRANSCRIPTION (patient's spoken notes):
{voice_text}

Combine these into a single comprehensive JSON with this structure:
{
    "medicines": [{"name": "...", "dosage": "...", "frequency": "...", "duration": "..."}],
    "diagnosis": "...",
    "doctor_name": "...",
    "hospital": "...",
    "date": "...",
    "notes": "combined notes from both sources"
}

Rules:
- If the voice note mentions additional medicines not in the document, add them
- If the voice note provides context about diagnosis or symptoms, add to notes
- Prefer document data for medicine names/dosage (more precise than speech)
- Return ONLY valid JSON, no markdown, no code blocks
"""


def _get_client() -> genai.Client:
    """Create a Gemini client."""
    settings = get_settings()
    return genai.Client(api_key=settings.GEMINI_API_KEY)


async def extract_from_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """
    Extract medical data from an image using Gemini 1.5 Flash Vision.

    Args:
        image_bytes: Raw image bytes.
        mime_type: MIME type of the image.

    Returns:
        Structured dict with extracted data.
    """
    client = _get_client()

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        types.Part.from_text(text=EXTRACTION_PROMPT),
                    ],
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,  # Low temperature for precise extraction
                max_output_tokens=2048,
            ),
        )

        raw_text = response.text.strip()
        # Clean potential markdown code blocks
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]  # Remove first line
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        extracted = json.loads(raw_text)
        logger.info(f"Agent 1: Extracted {len(extracted.get('medicines', []))} medicines from image")
        return extracted

    except json.JSONDecodeError as e:
        logger.error(f"Agent 1: Failed to parse JSON response: {e}")
        logger.debug(f"Raw response: {raw_text}")
        return {
            "medicines": [],
            "diagnosis": None,
            "doctor_name": None,
            "hospital": None,
            "date": None,
            "notes": f"Extraction failed — raw text: {raw_text[:500]}",
        }
    except Exception as e:
        logger.error(f"Agent 1: Gemini API error: {e}")
        raise


async def extract_from_pdf_bytes(pdf_bytes: bytes) -> dict:
    """
    Extract medical data from a PDF using Gemini 1.5 Flash Vision.
    Gemini can natively handle PDF files.

    Args:
        pdf_bytes: Raw PDF file bytes.

    Returns:
        Structured dict with extracted data.
    """
    client = _get_client()

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                        types.Part.from_text(text=EXTRACTION_PROMPT),
                    ],
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2048,
            ),
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        extracted = json.loads(raw_text)
        logger.info(f"Agent 1: Extracted {len(extracted.get('medicines', []))} medicines from PDF")
        return extracted

    except json.JSONDecodeError as e:
        logger.error(f"Agent 1: Failed to parse JSON from PDF response: {e}")
        return {
            "medicines": [],
            "diagnosis": None,
            "doctor_name": None,
            "hospital": None,
            "date": None,
            "notes": f"PDF extraction failed — raw text: {raw_text[:500]}",
        }
    except Exception as e:
        logger.error(f"Agent 1: Gemini API error (PDF): {e}")
        raise


async def merge_with_transcription(extracted_data: dict, voice_text: str) -> dict:
    """
    Merge document extraction data with voice note transcription
    using Gemini 1.5 Flash.

    Args:
        extracted_data: Output from extract_from_image or extract_from_pdf_bytes.
        voice_text: Transcription text from Whisper.

    Returns:
        Merged structured dict.
    """
    if not voice_text or not voice_text.strip():
        return extracted_data

    client = _get_client()

    prompt = MERGE_PROMPT.format(
        doc_data=json.dumps(extracted_data, indent=2),
        voice_text=voice_text,
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        merged = json.loads(raw_text)
        logger.info("Agent 1: Successfully merged document + voice data")
        return merged

    except Exception as e:
        logger.error(f"Agent 1: Merge failed, returning document data only: {e}")
        # If merge fails, return the original extraction — don't lose data
        if extracted_data.get("notes"):
            extracted_data["notes"] += f"\n\n[Voice note]: {voice_text}"
        else:
            extracted_data["notes"] = f"[Voice note]: {voice_text}"
        return extracted_data
