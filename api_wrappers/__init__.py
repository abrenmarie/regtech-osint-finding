import streamlit as st
import os

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY")

if GEMINI_API_KEY:
    print(f"Ключ Gemini найден: {GEMINI_API_KEY[:4]}***")
if DEEPSEEK_API_KEY:
    print(f"Ключ DeepSeek найден: {DEEPSEEK_API_KEY[:4]}***")