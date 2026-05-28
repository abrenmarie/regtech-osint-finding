import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

class DaDataClient:
    def __init__(self):
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent
        project_root = parent_dir.parent

        env_path = project_root / '.env'
        
        print(f"Поиск .env здесь: {env_path}")
        print(f"Корень проекта: {project_root}")
        
        load_dotenv(dotenv_path=env_path)
        
        self.token = os.getenv("DADATA_API_KEY")
        self.secret = os.getenv("DADATA_SECRET_KEY")

        if not self.token:
            print("Ключ все еще не виден!")
        else:
            print(f"Ключ найден: {self.token[:5]}***")

        self.url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.token}",
            "X-Secret": f"{self.secret}"
        }

    def fetch_company(self, inn):
        data = {"query": inn}
        try:
            response = requests.post(self.url, json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json().get('suggestions')
                return result[0]['data'] if result else "Компания не найдена"
            return f"Ошибка API: {response.status_code}"
        except Exception as e:
            return f"Ошибка соединения: {e}"

if __name__ == "__main__":
    client = DaDataClient()
    inn = "7707083893"
    company = client.fetch_company(inn)
    
    if isinstance(company, dict):
        print(f"Найдено: {company.get('name', {}).get('full_with_opf')}")

        report_name = f"report_{inn}.json"
        with open(report_name, "w", encoding="utf-8") as f:
            json.dump(company, f, ensure_ascii=False, indent=4)
        print(f"Отчет сохранен в файл: {report_name}")
    else:
        print(f"Что-то пошло не так: {company}")