import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DADATA_API_KEY = os.getenv("DADATA_API_KEY")
    DADATA_SECRET_KEY = os.getenv("DADATA_SECRET_KEY")
    OPENSANCTIONS_API_KEY = os.getenv("OPENSANCTIONS_API_KEY")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DB_NAME = "regtech_data.db"
    
    RISK_WEIGHTS = {
        "sanctions_hit": 100,
        "new_domain": 20,
        "negative_news": 15,
        "invalid_status": 30
    }

    RISK_THRESHOLD_HIGH = 70
    RISK_THRESHOLD_MEDIUM = 40

    MAX_NEWS_COUNT = 10
    USER_AGENT = "RegTechComplianceBot/1.0"

    RISK_WEIGHTS = {
        "sanctions_hit": 100,
        "cbr_blacklist": 100,
        "bankruptcy": 80,
        "new_domain": 20,
        "negative_news": 15,
        "invalid_status": 30
    }