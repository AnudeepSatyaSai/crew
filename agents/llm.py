# agents/llm.py
import json
import google.generativeai as genai

genai.configure(api_key="AIzaSyAbk0Z3zh2a1aXnQXlbzJ94SEpul7vD_Gg")
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

class LLMAgent:
    def __init__(self, context):
        self.context = context

    def summarize(self):
        prompt = f"Summarize this multi-agent financial analysis:\n{json.dumps(self.context, indent=2)}"
        return gemini_model.generate_content(prompt).text.strip()

    def generate_factors(self):
        prompt = f"Based on this analysis, suggest 3 new quantitative factors to include in a trading strategy:\n{json.dumps(self.context, indent=2)}"
        return gemini_model.generate_content(prompt).text.strip()
