import requests
from bs4 import BeautifulSoup

class NewsScanner:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    def check_negative(self, company_name):
        url = f"https://html.duckduckgo.com/html/?q={company_name}+суд+штраф+скандал"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                titles = [a.get_text() for a in soup.find_all('a', class_='result__a')[:5]]
                return titles
            return []
        except:
            return []