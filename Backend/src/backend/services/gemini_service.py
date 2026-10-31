import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT/".env")

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-flash-latest"

def test_gemini_connection():
    response=client.models.generate_content(
        model = MODEL_NAME,
        contents ="Explain what an incident management system does in two sentences"
    )
    return response.text

if __name__ == "__main__":
    result = test_gemini_connection()
    print("Gemini Response:")
    print(result)