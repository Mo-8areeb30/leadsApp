from flask import Flask, request, jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask("leadsApp")

# Database connection
conn = sqlite3.connect('leads_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        business TEXT
    )
''')
conn.commit()

# Email configuration
email_host = 'email_host'
email_port = 587
email_username = 'email_username'
email_password = 'email_password'
commercial_team_email = 'commercial_team@gmail.com'

def send_email(subject, body):
    """
    Sends an email with the provided subject and body to the commercial team.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_username
    msg['To'] = commercial_team_email

    with smtplib.SMTP(email_host, email_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, [commercial_team_email], msg.as_string())

# Endpoint to handle both POST and GET requests for /leads
@app.route('/leads', methods=['POST', 'GET'])
def handle_leads():
    """
    Handles requests related to leads. Supports both adding new leads (POST) and retrieving all leads (GET).
    """
    if request.method == 'POST':
        data = request.json
        name, email, phone, business = data['name'], data['email'], data['phone'], data['business']

        # Insert data into the database
        cursor.execute('INSERT INTO leads (name, email, phone, business) VALUES (?, ?, ?, ?)', (name, email, phone, business))
        conn.commit()

        # Send email to commercial team
        email_subject = 'New Lead'
        email_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nBusiness: {business}"
        send_email(email_subject, email_body)

        return jsonify({"message": "Lead added successfully!"}), 201
    elif request.method == 'GET':
        cursor.execute('SELECT * FROM leads')
        leads = cursor.fetchall()
        return jsonify(leads)

# Endpoint to retrieve individual lead by ID
@app.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """
    Retrieves an individual lead based on the provided lead ID.
    """
    cursor.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
    lead = cursor.fetchone()

    if lead:
        return jsonify(lead)
    else:
        return jsonify({"error": "Lead not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
