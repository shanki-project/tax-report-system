from flask import Flask, request, jsonify
import sqlite3
import os
import requests
from datetime import datetime

app = Flask(__name__)

NOTIFICATION_SERVICE_URL = "http://localhost:5005/notify"
DB_PATH = "../reports/tax_reports.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            pan_number TEXT NOT NULL,
            annual_income REAL NOT NULL,
            final_filename TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("[DB Service] Database initialized")

@app.route('/store', methods=['POST'])
def store_record():
    data = request.get_json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports 
        (first_name, last_name, email, pan_number, annual_income, final_filename, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['first_name'],
        data['last_name'],
        data['email'],
        data['pan_number'],
        data['annual_income'],
        data['final_filename'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    conn.commit()
    conn.close()
    print(f"[DB Service] Record stored for {data['first_name']} {data['last_name']}")

    # Forward to notification service
    try:
        response = requests.post(NOTIFICATION_SERVICE_URL, json=data)
        result = response.json()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reach notification service: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(port=5004, debug=True)