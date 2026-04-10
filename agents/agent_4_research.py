"""
Agent 4 — Web Research

Model: Gemini 1.5 Flash + Google Search Grounding
Purpose:
  - Receives medicine names from Agent 1
  - Searches the web for real current prices in India (brand vs generic)
  - Finds CDSCO approval status
  - Returns structured price and availability data
  - Runs concurrently with Agent 2's analysis
"""

import json
import logging
from google import genai
from google.genai import types
from core.config import get_settings

logger = logging.getLogger(__name__)

RESEARCH_PROMPT = """You are a pharmaceutical research assistant for the Indian market.

For each of the following medicines, search the web and find:
1. Current market price in India (MRP in ₹)
2. Generic alternatives available in India with their prices
3. CDSCO (Central Drugs Standard Control Organisation) approval status
4. Manufacturer information
5. Availability status
6. Formulation type — e.g. tablet, capsule, syrup, injection, cream, inhaler
7. Therapeutic category — e.g. antibiotic, NSAID, antihypertensive, antidiabetic, antacid

Medicines to research:
{medicine_list}

Return ONLY valid JSON (no markdown, no code blocks) with this structure:
{{
    "medicines": [
        {{
            "original_name": "brand name as provided",
            "original_price_inr": 150.0,
            "generic_name": "generic/salt name",
            "formulation_type": "tablet",
            "therapeutic_category": "antibiotic",
            "generic_alternatives": [
                {{
                    "name": "alternative brand/generic name",
                    "price_inr": 45.0,
                    "manufacturer": "company name",
                    "cdsco_approved": true,
                    "formulation_type": "tablet",
                    "formulation_match": true
                }}
            ],
            "cdsco_approved": true,
            "availability": "widely available / limited / prescription only"
        }}
    ]
}}

Rules:
- Prices MUST be in Indian Rupees (₹ / INR)
- Focus on Indian pharmaceutical market only
- Include at least 2-3 generic alternatives per medicine if available
- If exact price is unknown, provide an approximate range
- formulation_match must be true ONLY if the alternative has the SAME formulation type as the original (e.g. both tablets)
- Be factual — if information is not found, set to null
"""


def _get_client() -> genai.Client:
    """Create a Gemini client."""
    settings = get_settings()
    return genai.Client(api_key=settings.GEMINI_API_KEY)


async def research_medicines(medicine_names: list[str]) -> dict:
    """
    Research medicine prices and alternatives using Gemini with Google Search Grounding.

    Args:
        medicine_names: List of medicine names to research.

    Returns:
        Dict with structured price/availability data.
    """
    if not medicine_names:
        return {"medicines": []}

    client = _get_client()
    medicine_list = "\n".join(f"- {name}" for name in medicine_names)
    prompt = RESEARCH_PROMPT.format(medicine_list=medicine_list)

    try:
        # Use Google Search grounding for real-time web data
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=4096,
                tools=[
                    types.Tool(google_search=types.GoogleSearch()),
                ],
            ),
        )

        raw_text = response.text.strip()
        # Clean markdown formatting if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        result = json.loads(raw_text)
        logger.info(
            f"Agent 4: Researched {len(result.get('medicines', []))} medicines "
            f"from web for: {medicine_names}"
        )
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Agent 4: Failed to parse research JSON: {e}")
        logger.debug(f"Raw response: {raw_text[:500]}")
        # Return partial data with raw text
        return {
            "medicines": [],
            "raw_response": raw_text[:1000],
            "error": "Failed to parse structured data from web research",
        }
    except Exception as e:
        logger.error(f"Agent 4: Web research error: {e}")
        return {
            "medicines": [],
            "error": str(e),
        }
