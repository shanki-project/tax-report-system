from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)

REPORTS_DIR = "../reports"

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(REPORTS_DIR, filename)

    if not os.path.exists(filepath):
        return jsonify({'error': f'File not found: {filename}'}), 404

    print(f"[Download Service] Serving file: {filename}")
    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

@app.route('/list', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.pdf')]
    return jsonify({'available_reports': files}), 200

if __name__ == '__main__':
    app.run(port=5006, debug=True)