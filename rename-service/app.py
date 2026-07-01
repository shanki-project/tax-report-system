from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

DB_SERVICE_URL = "http://localhost:5004/store"
REPORTS_DIR = "../reports"

@app.route('/rename', methods=['POST'])
def rename_file():
    data = request.get_json()

    temp_filename = data['temp_filename']
    first_name = data['first_name']
    last_name = data['last_name']
    date_str = datetime.now().strftime('%Y%m%d')

    new_filename = f"{date_str}_{first_name}_{last_name}.pdf"
    temp_filepath = os.path.join(REPORTS_DIR, temp_filename)
    new_filepath = os.path.join(REPORTS_DIR, new_filename)

    os.rename(temp_filepath, new_filepath)
    print(f"[Rename Service] Renamed to: {new_filename}")

    # Forward to DB service
    try:
        response = requests.post(DB_SERVICE_URL, json={
            **data,
            'final_filename': new_filename
        })
        result = response.json()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reach db service: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)