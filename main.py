import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

import database_manager
from api_wrappers.dadata_wrapper import DaDataClient
from osint_tools.news_parser import NewsScanner
from osint_tools.domain_checker import DomainInvestigator
from osint_tools.sanctions_checker import SanctionsChecker
from osint_tools.risk_analyser import RiskAnalyser
from osint_tools.cbr_checker import CBRChecker
from config import Config

def run_compliance_check(query, domain=None):
    try:
        dadata = DaDataClient()
        scanner = NewsScanner()
        sanctions_checker = SanctionsChecker()
        cbr = CBRChecker()
        
        company_data = dadata.get_company_info(query)
        if company_data:
            company_name = company_data.get('name', query)
            inn = company_data.get('inn', "Н/Д")
            company_status = company_data.get('state', {}).get('status', 'ACTIVE')
        else:
            company_name = query
            inn = "Н/Д"
            company_status = "ACTIVE"

        sanctions_results = sanctions_checker.check_entity(company_name)
        
        news = scanner.check_negative(company_name)
        
        age_days = 0
        if domain:
            investigator = DomainInvestigator()
            dom_res = investigator.check_domain(domain)
            if isinstance(dom_res, dict):
                age_days = dom_res.get('age_days', 0)

        is_illegal = cbr.check_blacklist(inn, company_name)

        analysis = RiskAnalyser.calculate_score(
            sanctions_results=sanctions_results,
            news_count=len(news),
            domain_age_days=age_days,
            company_status=company_status,
            is_cbr_blacklisted=is_illegal
        )
        
        return company_name, inn, age_days, news, analysis, sanctions_results

    except Exception as e:
        print(f"Критическая ошибка в run_compliance_check: {e}")
        return query, "Ошибка", 0, [], {"level": "UNKNOWN", "score": 0, "reasons": [str(e)]}, []

if __name__ == "__main__":
    database_manager.init_db(Config.DB_NAME)
    test_query = "7707083893" 
    print(f"--- Тестовая проверка: {test_query} ---")

    result = run_compliance_check(test_query, domain="sberbank.ru")
    
    if result:
        name, inn, age, news_list, analysis, sanctions = result
        print(f"Объект: {name}")
        print(f"Скоринг: {analysis['score']}/100")
        print(f"Риск: {analysis['level']}")
    else:
        print("Ошибка теста.")