import os
import sys
import streamlit as st

try:
    import google.genai as genai
except ImportError:
    try:
        genai = __import__('google.genai', fromlist=['*'])
    except ImportError as e:
        raise ImportError(f"Сбой импорта google-genai. Проверьте requirements.txt. Ошибка: {e}")

class LLMNewsAnalyzer:
    def __init__(self):
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in secrets or environment")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    def analyze_negative_context(self, news_list, company_name):
        if not news_list:
            return "No text provided for analysis."

        context = "\n".join([f"- {news}" for news in news_list])
        
        prompt = f"""
        Analyze the following news context regarding the entity '{company_name}' for compliance, regulatory, and reputational risks.
        Provide a concise risk verdict in Russian.
        
        Context:
        {context}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.2}
            )
            return response.text if response.text else "API returned an empty response."
        except Exception as e:
            return f"Gemini API Error: {str(e)}"