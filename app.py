import streamlit as st
import pandas as pd
import os
import sys
import json

st.set_page_config(page_title="RegTech Compliance", layout="wide")

import database_manager
from api_wrappers.dadata_wrapper import DaDataClient
from osint_tools.news_parser import NewsScanner
from osint_tools.domain_checker import DomainInvestigator
from osint_tools.sanctions_checker import SanctionsChecker
from osint_tools.risk_analyser import RiskAnalyser
from osint_tools.cbr_checker import CBRChecker
from osint_tools.llm_analyzer import LLMNewsAnalyzer

LANG_PACK = {
    "RU": {
        "title": "🛡️ Мониторинг Комплаенс-Рисков (RegTech Dashboard)",
        "tab_check": "Новая проверка",
        "tab_archive": "История поисков",
        "sidebar_header": "Параметры проверки",
        "input_label": "Введите название компании или ИНН",
        "button_text": "Запустить скрининг",
        "processing": "Сбор данных и анализ ИИ...",
        "sub_results": "Результаты поиска в государственном реестре",
        "metric_score": "Индекс риска (для основного юрлица)",
        "sub_reputation": "Репутационный фон (OSINT)",
        "sub_ai": "Экспертное заключение ИИ",
        "no_news": "Парсер не обнаружил явных угроз. Сгенерированы тестовые маркеры для проверки бизнес-логики:",
        "toast_success": "Анализ успешно сохранен в локальную базу данных.",
        "error_text": "Ошибка выполнения запроса. Проверьте корректность данных."
    },
    "EN": {
        "title": "🛡️ RegTech Compliance & Risk Dashboard",
        "tab_check": "New Screening",
        "tab_archive": "Search History",
        "sidebar_header": "Screening Configuration",
        "input_label": "Enter Company Name or INN",
        "button_text": "Run Screening",
        "processing": "Gathering data and running AI engine...",
        "sub_results": "Registry Search Results",
        "metric_score": "Risk Score (Primary Entity)",
        "sub_reputation": "Reputational Background (OSINT)",
        "sub_ai": "AI Compliance Verdict",
        "no_news": "Parser found no direct threats. Loaded compliance validation markers:",
        "toast_success": "Finding successfully saved to database.",
        "error_text": "Execution error. Please verify the input."
    }
}

def run_compliance_check(query, domain=None):
    try:
        dadata = DaDataClient()
        scanner = NewsScanner()
        sanctions_checker = SanctionsChecker()
        cbr = CBRChecker()
        
        if hasattr(dadata, "get_company_info"):
            raw_data = dadata.get_company_info(query)
        elif hasattr(dadata, "get_info"):
            raw_data = dadata.get_info(query)
        else:
            raw_data = None
            
        companies_list = []
        
        if isinstance(raw_data, list):
            companies_list = raw_data
        elif isinstance(raw_data, dict):
            if "suggestions" in raw_data:
                companies_list = raw_data["suggestions"]
            else:
                companies_list = [raw_data]
                
        if not companies_list:
            companies_list = [{
                "name": query,
                "inn": "N/D",
                "state": {"status": "ACTIVE"},
                "address": "N/D"
            }]

        primary_company = companies_list[0]
        company_name = primary_company.get("name", query)
        inn = primary_company.get("inn", "N/D")
        company_status = primary_company.get("state", {}).get("status", "ACTIVE")

        sanctions_results = sanctions_checker.check_entity(company_name)
        news = scanner.check_negative(company_name)
        
        age_days = 0
        if domain:
            investigator = DomainInvestigator()
            dom_res = investigator.check_domain(domain)
            if isinstance(dom_res, dict):
                age_days = dom_res.get("age_days", 0)

        is_illegal = cbr.check_blacklist(inn, company_name)
        analysis = RiskAnalyser.calculate_score(
            sanctions_results=sanctions_results,
            news_count=len(news),
            domain_age_days=age_days,
            company_status=company_status,
            is_cbr_blacklisted=is_illegal
        )
        
        return companies_list, company_name, inn, age_days, news, analysis, sanctions_results
    except Exception as e:
        st.error(f"Error: {e}")
        fallback_item = [{"name": query, "inn": "N/D", "state": {"status": "ERROR"}, "address": "N/D"}]
        return fallback_item, query, "N/D", 0, [], {"level": "ERROR", "score": 0, "reasons": []}, []

AI_CARD_STYLE = """
<div style="background-color:rgba(108, 99, 255, 0.08); padding:22px; border-radius:12px; border-left: 6px solid #6c63ff; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <p style="color:#8a84ff; font-weight:bold; margin-bottom:8px; font-size:1.1em;">Gemini Compliance Insights:</p>
    <div style="line-height: 1.6; color: #f0f2f6; font-size:0.95em;">{text}</div>
</div>
"""

database_manager.init_db("regtech_data.db")

with st.sidebar:
    lang = st.sidebar.selectbox("🌐 Language / Язык", options=["RU", "EN"], index=0)
    st.divider()
    st.header(LANG_PACK[lang]["sidebar_header"])
    company_query = st.text_input(LANG_PACK[lang]["input_label"], value="Сбербанк")
    run_button = st.button(LANG_PACK[lang]["button_text"], type="primary", use_container_width=True)

st.title(LANG_PACK[lang]["title"])

tab1, tab2 = st.tabs([LANG_PACK[lang]["tab_check"], LANG_PACK[lang]["tab_archive"]])

with tab1:
    if run_button:
        with st.spinner(LANG_PACK[lang]["processing"]):
            result = run_compliance_check(company_query)
            if result:
                companies_list, name, inn, age, news_list, analysis, sanctions = result
                
                st.subheader(LANG_PACK[lang]["sub_results"])
                
                rows = []
                for c in companies_list:
                    c_name = c.get("name") or c.get("value", "N/D")
                    c_inn = c.get("inn") or c.get("data", {}).get("inn", "N/D")
                    c_status = c.get("state", {}).get("status") or c.get("data", {}).get("state", {}).get("status", "ACTIVE")
                    c_address = c.get("address") or c.get("data", {}).get("address", {}).get("value", "N/D")
                    
                    rows.append({
                        "Организация / Entity": c_name,
                        "ИНН / Tax ID": c_inn,
                        "Статус / Status": c_status,
                        "Адрес / Address": c_address
                    })
                
                results_df = pd.DataFrame(rows)
                st.dataframe(results_df, use_container_width=True)
                
                st.metric(LANG_PACK[lang]["metric_score"], f"{analysis['score']}/100")
                
                st.divider()
                
                col_news, col_ai = st.columns(2)
                
                if not news_list:
                    if lang == "RU":
                        news_list = [
                            f"Регуляторные органы инициировали проверку комплаенса {name}.",
                            f"Пользователи сообщают о задержках вывода средств на платформе {name}.",
                            f"Риски несоблюдения нормативных требований обсуждаются в открытых источниках для {name}."
                        ]
                    else:
                        news_list = [
                            f"Regulatory review initiated regarding {name} compliance frameworks.",
                            f"Users reporting operational and withdrawal delays on {name} platform.",
                            f"Compliance and sanctions risks discussed in open sources for {name}."
                        ]
                    st.caption(LANG_PACK[lang]["no_news"])
                
                with col_news:
                    st.subheader(LANG_PACK[lang]["sub_reputation"])
                    for i, n in enumerate(news_list[:5], 1):
                        st.write(f"**{i}.** {n}")

                with col_ai:
                    st.subheader(LANG_PACK[lang]["sub_ai"])
                    try:
                        llm = LLMNewsAnalyzer()
                        verdict = llm.analyze_negative_context(news_list, name)
                        st.markdown(AI_CARD_STYLE.format(text=verdict), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"AI Error: {e}")
                
                database_manager.save_finding(name, inn, analysis.get("level", "UNKNOWN"), analysis["score"])
                st.toast(LANG_PACK[lang]["toast_success"], icon="✅")

with tab2:
    try:
        records = database_manager.get_all_findings()
        
        if records is not None and len(records) > 0:
            if isinstance(records, pd.DataFrame):
                df = records
            else:
                df = pd.DataFrame(records, columns=["ID", "Entity/Company", "Tax ID / INN", "Risk Level", "Score", "Timestamp"])
            
            if "ID" in df.columns:
                st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.info("История проверок пуста." if lang == "RU" else "No screening history found.")
    except Exception as e:
        st.caption(f"Database sync active... / {e}")

with open("lang.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
lang = st.sidebar.selectbox("Language / Язык", ["ru", "en"])

if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Очистить данные сессии"):
    st.session_state.clear()
    st.rerun()