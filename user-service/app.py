from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REPORT_SERVICE_URL = "http://localhost:5002/generate"

@app.route('/user', methods=['POST'])
def accept_user():
    data = request.get_json()

    # Basic validation
    required_fields = ['first_name', 'last_name', 'email', 'pan_number', 'annual_income']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    print(f"[User Service] Received user: {data['first_name']} {data['last_name']}")

    # Forward to report service
    try:
        response = requests.post(REPORT_SERVICE_URL, json=data)
        result = response.json()
        return jsonify({
            'message': 'User received and report triggered',
            'report_details': result
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reach report service: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)