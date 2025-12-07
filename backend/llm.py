import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")


class GeminiLLMWrapper:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

        genai.configure(api_key=api_key)

        # ✅ FREE-TIER SAFE & STABLE MODEL
        self.llm = genai.GenerativeModel("models/gemini-flash-latest")

        print("✅ LLM ready with model: models/gemini-flash-latest")

    def invoke(self, prompt: str) -> str:
        response = self.llm.generate_content(prompt)
        return response.text


def get_gemini_llm():
    return GeminiLLMWrapper()
