import sqlite3
import pandas as pd
from datetime import datetime

def init_db(db_name="regtech_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            inn TEXT,
            risk_level TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_finding(name, inn, risk_level, score):
    conn = sqlite3.connect("regtech_data.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO findings (timestamp, name, inn, risk_level, score)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, name, inn, risk_level, score))
    conn.commit()
    conn.close()

def get_all_findings():
    conn = sqlite3.connect("regtech_data.db")
    df = pd.read_sql_query("SELECT * FROM findings ORDER BY timestamp DESC", conn)
    conn.close()
    return df