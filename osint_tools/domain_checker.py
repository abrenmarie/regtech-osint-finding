import whois
from datetime import datetime, timezone

class DomainInvestigator:
    def check_domain(self, domain_url):
        print(f"Investigating domain: {domain_url}...")
        try:
            w = whois.whois(domain_url)
            creation_date = w.creation_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                if creation_date.tzinfo is not None:
                    creation_date = creation_date.astimezone(timezone.utc)
                else:
                    creation_date = creation_date.replace(tzinfo=timezone.utc)

                now = datetime.now(timezone.utc)
                
                age_days = (now - creation_date).days
                return {
                    "creation_date": creation_date.strftime("%Y-%m-%d"),
                    "age_days": age_days,
                    "is_risk": age_days < 365
                }
            return "Creation date not found"
        except Exception as e:
            return f"WHOIS Error: {e}"

if __name__ == "__main__":
    investigator = DomainInvestigator()
    result = investigator.check_domain("sberbank.ru")
    print(result)