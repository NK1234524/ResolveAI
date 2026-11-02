
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from pydantic import ValidationError

from backend.schemas.ai_assessment import IncidentAssessment


PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-flash-latest"


def test_gemini_connection():
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Explain what an incident management system does in two sentences"
    )
    return response.text


def analyze_incident(incident_report: str):
    prompt = f"""
    You are an incident assessment assistant for ResolveAI.

    Analyze the incident report and extract structured information.

    Instructions:

    1. Generate a concise incident title.
    2. Provide a clear incident description.
    3. Select exactly one category from:
       NETWORK, HARDWARE, SOFTWARE, SECURITY,
       ACCESS, INFRASTRUCTURE, OTHER.

    4. Select impact from:
       LOW, MEDIUM, HIGH, CRITICAL.

    5. Select urgency from:
       LOW, MEDIUM, HIGH, CRITICAL.

    6. Extract the location only if mentioned.
       Otherwise return null.

    7. Extract the deadline only when both the date
       and time can be determined.

    8. Return the deadline in ISO 8601 datetime format.

    9. If only a time is mentioned, return null.

    10. Never invent missing information.

    11. Use only the exact uppercase Enum values
        specified above.

    Incident Report:
    {incident_report}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=IncidentAssessment,
                temperature=0.2
            )
        )

        if response.parsed is None:
            raise ValueError(
                "Gemini returned an empty or invalid response"
            )

        validated_data = IncidentAssessment.model_validate(
            response.parsed
        )

        return validated_data

    # Exception handling for Gemini errors
    except httpx.RemoteProtocolError as e :
        raise RuntimeError(
            "Gemini connection was interrupted.please try later."
        )
    except ValidationError as e:
        raise ValueError(
            "Gemini returned data that failed validation."
        ) from e

    except httpx.TimeoutException as e:
        raise RuntimeError(
            "Gemini request timed out. Please try again."
        ) from e

    except errors.APIError as e:
        if e.code == 429:
            raise RuntimeError(
                "Gemini rate limit exceeded. Please try again later."
            ) from e

        elif e.code in (401, 403):
            raise RuntimeError(
                "Gemini authentication failed. Check API configuration."
            ) from e

       

        elif e.code == 503:
            raise RuntimeError(
                "Gemini is temporarily unavailable.Try again later!!"
            )

        else:
            raise RuntimeError(
                f"Gemini API error: {e.message or 'Request failed'}"
            ) from e


if __name__ == "__main__":
    report = """The projector in classroom 204 is not working.
The teacher is unable to display the presentation.
"""

    result = analyze_incident(report)
    print(result.model_dump_json(indent=2))
