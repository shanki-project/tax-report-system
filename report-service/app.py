from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import requests
import os
from datetime import datetime

app = Flask(__name__)

RENAME_SERVICE_URL = "http://localhost:5003/rename"
REPORTS_DIR = "../reports"

@app.route('/generate', methods=['POST'])
def generate_report():
    data = request.get_json()

    print(f"[Report Service] Generating report for {data['first_name']} {data['last_name']}")

    # Generate PDF
    temp_filename = f"temp_{data['pan_number']}.pdf"
    temp_filepath = os.path.join(REPORTS_DIR, temp_filename)

    # Calculate fake tax details
    annual_income = float(data['annual_income'])
    tax_rate = 0.30 if annual_income > 1000000 else 0.20 if annual_income > 500000 else 0.10
    tax_amount = annual_income * tax_rate
    net_income = annual_income - tax_amount

    # Build PDF
    doc = SimpleDocTemplate(temp_filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("INCOME TAX REPORT 2024-25", styles['Title']))
    elements.append(Spacer(1, 20))

    # User details table
    user_data = [
        ['Field', 'Details'],
        ['Name', f"{data['first_name']} {data['last_name']}"],
        ['Email', data['email']],
        ['PAN Number', data['pan_number']],
        ['Annual Income', f"Rs. {annual_income:,.2f}"],
        ['Tax Rate', f"{tax_rate * 100:.0f}%"],
        ['Tax Amount', f"Rs. {tax_amount:,.2f}"],
        ['Net Income', f"Rs. {net_income:,.2f}"],
        ['Generated On', datetime.now().strftime('%d-%m-%Y %H:%M:%S')],
    ]

    table = Table(user_data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white]),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("This is a system generated report.", styles['Normal']))

    doc.build(elements)
    print(f"[Report Service] PDF created: {temp_filepath}")

    # Forward to rename service
    try:
        response = requests.post(RENAME_SERVICE_URL, json={
            **data,
            'temp_filename': temp_filename
        })
        result = response.json()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reach rename service: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)