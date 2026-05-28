# 🛡️ RegTech Compliance & Risk Screening Dashboard

An automated Governance, Risk, and Complance (GRC) and Open Source Intelligence (OSINT) platform designed to streamline corporate screening, anti-money laundering (AML), and know-your-customer (KYC) workflows. The application aggregates data from official state registries, open-source news feeds, and utilizes generative AI (Google Gemini 2.5) to deliver real-time risk assessments.

## Key Features

- **Multi-Row Registry Search:** – Queries government databases via DaData API by Company Name or Tax ID (INN), handling ambiguous queries and displaying comprehensive legal entitles data (names, status, registration addresses).
- **OSINT & Reputational Scraper:** – Automatically scans media sources for adverse keywords and negative news regarding the target entity.
- **Risk Scoring Engine:** – Dynamically calculates a weighted risk score (0-100) based on sanctions listings, CBR blacklists, domain age verification, corporate status, and adverse media presence.
- **AI-Driven Compliance Verdict:** – Integrates the state-of-the-art **Gemini 2.5 Flash** model via the official 'google-genai' client to analyze negative context, offering structured summaries on regulatory, operational, and financial crime risks.
- **Internationalization (i18n):** – Features a full-fledged language switcher (RU/EN) within the interface, adjusting both UI text and LLM instructions dynamically.
- **Local Auditing & Archive:** – Automatically logs every screening session into an embedded SQLite database using standart SQL queries for historical compliance audits.

## Tech Stack

- **Language:** Python 3.14+
- **Frontend/UI:** Streamlit Framework
- **AI Orchestration:** Google GenAI SDK (Gemini 2.5 Flash)
- **Data Engineering:** Pandas, SQLite3
- **Integrations:** DaData API (Rest Client)
- **Environment:** Fully containerized with VS Code DevConteiners, dependency management handled via 'uv' package installer.

## Core Architecture Flow

1. **Input:** User submits an entity name or INN through the Streamlit UI.
2. **Data Aggregation:** Parallel data fetching from DaDataAPI + Local Sanctions/CBR Checkers.
3. **OSINT Analysis:** Extraction of adverse news context.
4. **LLM Evaluation:** Gemini 2.5 Flash processes the text array and outputs an expert risk verdict.
5. **Persistence:** Data is stored in SQLite; results are rendered dynamically on the web UI.

## Prerequisites

- Python 3.9 - 3.14
- Docker Desktop (Optional, for DevContainers)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone (https://github.com/abrenmarie/regtech-osint-finding.git)
   cd regtech-osint-finding
   ```

2. **Set up a virtual environment and install dependencies:**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # MacOS/Linux
   venv/Scripts/activate  # Windows
   ```

3. **Install dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

Create a .env file in the root directory and populate your keys
   
   ```bash
   DADATA_API_KEY=your_dadata_key
   DADATA_SECRET_KEY=your_dadata_secret
   OPENSANCTIONS_API_KEY=your_opensanctions_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the application:**

   ```bash
   streamlit run app.py
   ```

**Deployment in Streamlit Cloud:**

To maintain functionally in production, specify the environment variables in the Streamlit Cloud dashboard under Advanced Settings -> Secrets:

   ```bash
   DADATA_API_KEY=your_key
   DADATA_SECRET_KEY=your_secret
   GEMINI_API_KEY=your_gemini_key
   ```

**License:**
This project is developed for educational and portfolio presentation purposes in the field of International Economics, Corporate Law, and RegTech Automation.