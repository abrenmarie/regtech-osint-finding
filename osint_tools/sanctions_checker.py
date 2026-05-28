import requests
import os
from dotenv import load_dotenv
from thefuzz import fuzz
from config import Config

load_dotenv()

class SanctionsChecker:
    def __init__(self):
        self.api_key = Config.OPENSANCTIONS_API_KEY
        self.base_url = "https://api.opensanctions.org/search/default"

    def check_entity(self, name):
        if not self.api_key:
            return []

        headers = {"Authorization": f"ApiKey {self.api_key}"}
        url = "https://api.opensanctions.org/match/default"
        
        payload = {
            "queries": {
                "q1": {
                    "schema": "Organization",
                    "properties": {
                        "name": [name]
                    }
                }
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            
            results = []
            responses = data.get('responses', {}).get('q1', {}).get('results', [])
            
            for item in responses:
                score = int(item.get('score', 0) * 100)
                
                if score > 70:
                    results.append({
                        "name": item.get('caption'),
                        "score": score,
                        "lists": item.get('datasets', []),
                    })
            return results
        except Exception as e:
            print(f"Sanctions check error: {e}")
            return []