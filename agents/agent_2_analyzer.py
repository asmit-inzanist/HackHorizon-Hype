"""
Agent 2 — Medicine Analyzer

Model: meta-llama/llama-3.3-70b-instruct:free via OpenRouter
Purpose:
  - Takes extracted medicine names from Agent 1
  - Calls Agent 4 concurrently for real-time web price verification
  - Combines web research data
  - Calculates actual rupee savings vs generic alternatives
  - Returns full comparison with safety equivalence check
"""

import json
import asyncio
import logging
import httpx
from core.config import get_settings
from agents.agent_4_research import research_medicines

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

ANALYZER_PROMPT = """You are a pharmaceutical analysis expert for the Indian market.

You have received web research data about medicines from a patient's prescription.
Analyze this data and provide a comprehensive comparison.

WEB RESEARCH DATA:
{web_data}

PATIENT'S PRESCRIBED MEDICINES:
{prescribed_medicines}

Analyze each medicine and return ONLY valid JSON (no markdown, no code blocks):
{{
    "medicines": [
        {{
            "original_name": "prescribed brand name",
            "original_price": 150.0,
            "generic_name": "active ingredient / salt name",
            "generic_alternatives": [
                {{
                    "name": "generic brand name",
                    "price": 45.0,
                    "manufacturer": "company",
                    "savings": 105.0
                }}
            ],
            "cdsco_approved": true,
            "safety_equivalent": true,
            "safety_notes": "brief note on equivalence"
        }}
    ],
    "total_savings": 250.0,
    "summary": "brief overall summary of savings potential"
}}

Rules:
- Calculate savings = original_price - generic_price for each alternative
- total_savings = sum of maximum possible savings across all medicines
- safety_equivalent should be true ONLY if the generic has the same active ingredient and dosage form
- All prices in Indian Rupees (₹)
- Sort alternatives by price (cheapest first)
- If no data available for a medicine, still include it with nulls
"""


async def _call_openrouter(prompt: str) -> str:
    """Call OpenRouter API with Llama 3.3 70B."""
    settings = get_settings()

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://health-record-platform.com",
        "X-Title": "Health Record Medicine Analyzer",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a pharmaceutical analysis expert. Always respond with valid JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]


async def analyze_medicines(extracted_data: dict) -> dict:
    """
    Analyze medicines from Agent 1's extraction.
    Runs Agent 4 (web research) concurrently, then feeds data to Llama 3.3
    for comparison and savings analysis.

    Args:
        extracted_data: Output from Agent 1 containing medicines list.

    Returns:
        Complete medicine analysis with alternatives and savings.
    """
    medicines = extracted_data.get("medicines", [])
    if not medicines:
        return {
            "medicines": [],
            "total_savings": 0.0,
            "summary": "No medicines found in the prescription.",
        }

    # Extract medicine names
    medicine_names = [m["name"] for m in medicines if m.get("name")]

    if not medicine_names:
        return {
            "medicines": [],
            "total_savings": 0.0,
            "summary": "Could not extract medicine names from the prescription.",
        }

    logger.info(f"Agent 2: Analyzing {len(medicine_names)} medicines: {medicine_names}")

    # ── Step 1: Run Agent 4 web research concurrently ──
    web_research_task = asyncio.create_task(research_medicines(medicine_names))

    # Wait for web research to complete
    web_data = await web_research_task

    # ── Step 2: Feed combined data to Llama 3.3 for analysis ──
    prompt = ANALYZER_PROMPT.format(
        web_data=json.dumps(web_data, indent=2),
        prescribed_medicines=json.dumps(medicines, indent=2),
    )

    try:
        raw_response = await _call_openrouter(prompt)

        # Clean markdown formatting
        raw_text = raw_response.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        analysis = json.loads(raw_text)
        logger.info(
            f"Agent 2: Analysis complete — "
            f"total savings: ₹{analysis.get('total_savings', 0)}"
        )
        return analysis

    except json.JSONDecodeError as e:
        logger.error(f"Agent 2: Failed to parse analysis JSON: {e}")
        # Fallback: return web research data directly
        return {
            "medicines": web_data.get("medicines", []),
            "total_savings": 0.0,
            "summary": "Analysis parsing failed. Raw web research data provided.",
            "raw_web_data": web_data,
        }
    except Exception as e:
        logger.error(f"Agent 2: OpenRouter API error: {e}")
        return {
            "medicines": [],
            "total_savings": 0.0,
            "summary": f"Analysis failed: {str(e)}",
            "raw_web_data": web_data,
        }
