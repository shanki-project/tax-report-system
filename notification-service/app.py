from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os

app = Flask(__name__)

DOWNLOAD_SERVICE_URL = "http://localhost:5006/download"
GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', 'your-email@gmail.com')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', 'your-app-password')

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()

    recipient_email = data['email']
    first_name = data['first_name']
    final_filename = data['final_filename']
    download_url = f"{DOWNLOAD_SERVICE_URL}/{final_filename}"

    # Build email
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = "Your Tax Report is Ready"

    body = f"""
Dear {first_name},

Your income tax report has been successfully generated.

Report filename : {final_filename}
Download link  : {download_url}

Please download your report using the link above.

Regards,
Tax Report System
    """

    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, recipient_email, msg.as_string())
        server.quit()
        print(f"[Notification Service] Email sent to {recipient_email}")
    except Exception as e:
        print(f"[Notification Service] Email failed: {str(e)}")

    return jsonify({
        'message': 'Notification sent',
        'download_url': download_url,
        'final_filename': final_filename
    }), 200

if __name__ == '__main__':
    app.run(port=5005, debug=True)