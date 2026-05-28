from config import Config

class RiskAnalyser:
    @staticmethod
    def calculate_score(sanctions_results, news_count, domain_age_days, 
                        company_status, is_cbr_blacklisted=False, is_bankrupt=False):
        score = 0
        reasons = []

        if is_cbr_blacklisted:
            score += Config.RISK_WEIGHTS["cbr_blacklist"]
            reasons.append("В списке нелегальных участников рынка ЦБ РФ")

        if sanctions_results:
            score += Config.RISK_WEIGHTS["sanctions_hit"]
            reasons.append("Найдено в глобальных санкционных списках")

        if is_bankrupt:
            score += Config.RISK_WEIGHTS["bankruptcy"]
            reasons.append("Зафиксирована процедура банкротства")

        if news_count > 0:
            news_penalty = news_count * Config.RISK_WEIGHTS["negative_news"]
            score += min(news_penalty, 40)
            reasons.append(f"Негативный фон: {news_count} упом.")

        if company_status and company_status != "ACTIVE":
            score += Config.RISK_WEIGHTS["invalid_status"]
            reasons.append(f"Статус организации: {company_status}")

        if 0 < domain_age_days < 180:
            score += Config.RISK_WEIGHTS["new_domain"]
            reasons.append("Риск: подозрительно молодой домен")

        final_score = min(score, 100)
        
        if final_score >= Config.RISK_THRESHOLD_HIGH:
            level = "CRITICAL"
        elif final_score >= Config.RISK_THRESHOLD_MEDIUM:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {"score": final_score, "level": level, "reasons": reasons}