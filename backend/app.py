import os
import csv
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Tuple
import io

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Configure CORS for local dev (adjust origins for production)
    CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000", "*"]}})

    def parse_csv_data(csv_content: str) -> List[Dict[str, str]]:
        """Parse CSV content and return list of dictionaries with company_name and email."""
        try:
            # Create a file-like object from the CSV content
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            # Validate required columns
            if 'company_name' not in reader.fieldnames or 'email' not in reader.fieldnames:
                raise ValueError("CSV must contain 'company_name' and 'email' columns")
            
            # Parse and validate data
            companies = []
            for row in reader:
                company_name = row.get('company_name', '').strip()
                email = row.get('email', '').strip()
                
                if company_name and email:
                    companies.append({
                        'company_name': company_name,
                        'email': email
                    })
            
            return companies
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")

    def personalize_message(template: str, company_name: str) -> str:
        """Replace {{company_name}} placeholder with actual company name."""
        return template.replace('{{company_name}}', company_name)

    def load_sent_log() -> List[Tuple[str, str]]:
        """Load existing sent emails from CSV log to check for duplicates."""
        log_file = 'sent_log.csv'
        sent_emails = []
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        sent_emails.append((row['company_name'], row['email']))
            except Exception as e:
                print(f"Warning: Could not read sent log: {e}")
        
        return sent_emails

    def log_sent_email(company_name: str, email: str) -> None:
        """Log successfully sent email to CSV file."""
        log_file = 'sent_log.csv'
        timestamp = datetime.now().isoformat()
        
        # Create file with headers if it doesn't exist
        file_exists = os.path.exists(log_file)
        
        try:
            with open(log_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['company_name', 'email', 'timestamp'])
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'company_name': company_name,
                    'email': email,
                    'timestamp': timestamp
                })
        except Exception as e:
            print(f"Warning: Could not write to sent log: {e}")

    def attach_resume(msg: MIMEMultipart, resume_path: str = './resume/my_resume.pdf') -> None:
        """Attach resume file to the email."""
        try:
            if os.path.exists(resume_path):
                with open(resume_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(resume_path)}'
                )
                msg.attach(part)
            else:
                print(f"Warning: Resume file not found at {resume_path}")
        except Exception as e:
            print(f"Warning: Could not attach resume: {e}")

    @app.route("/health", methods=["GET"])
    def health() -> Any:
        return jsonify({"status": "ok"})

    @app.route("/", methods=["GET"])
    def index() -> Any:
        # Serve the frontend
        return render_template("index.html")

    @app.route("/send-emails", methods=["POST"])
    def send_emails() -> Any:
        data = request.get_json(silent=True) or {}
        csv_content: str = data.get("csv_content") or ""
        subject: str = (data.get("subject") or "").strip()
        message_template: str = data.get("message") or ""

        if not csv_content or not subject or not message_template:
            return (
                jsonify({
                    "error": "Missing required fields",
                    "details": {
                        "csv_content": bool(csv_content),
                        "subject": bool(subject),
                        "message": bool(message_template),
                    },
                }),
                400,
            )

        # Load credentials from environment
        gmail_user = os.getenv("GMAIL_USER")
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_app_password:
            return (
                jsonify({
                    "error": "Server email credentials are not configured",
                    "hint": "Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.",
                }),
                500,
            )

        try:
            # Parse CSV data
            companies = parse_csv_data(csv_content)
            if not companies:
                return jsonify({"error": "No valid company data found in CSV"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        # Load existing sent emails to check for duplicates
        sent_emails = load_sent_log()
        sent_emails_set = set(sent_emails)

        # Filter out already sent emails
        new_companies = []
        skipped = []
        for company in companies:
            if (company['company_name'], company['email']) in sent_emails_set:
                skipped.append(company)
            else:
                new_companies.append(company)

        if not new_companies:
            return jsonify({
                "message": "All emails have already been sent",
                "sent": [],
                "failed": [],
                "skipped": [{"company_name": c["company_name"], "email": c["email"]} for c in skipped]
            })

        sent: List[Dict[str, str]] = []
        failed: List[Dict[str, str]] = []

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_app_password)
        except Exception as e:  # SMTP login failure
            return (
                jsonify({
                    "error": "SMTP login failed",
                    "details": str(e),
                }),
                502,
            )

        # Send personalized emails to each recipient
        for company in new_companies:
            try:
                msg = MIMEMultipart('alternative')
                msg['From'] = gmail_user
                msg['To'] = company['email']
                msg['Subject'] = subject

                # Personalize the message
                personalized_message = personalize_message(message_template, company['company_name'])
                
                # HTML part
                html_part = MIMEText(personalized_message, 'html')
                msg.attach(html_part)

                # Attach resume
                attach_resume(msg)

                server.sendmail(gmail_user, [company['email']], msg.as_string())
                
                # Log successful send
                log_sent_email(company['company_name'], company['email'])
                
                sent.append({
                    "company_name": company['company_name'],
                    "email": company['email']
                })
            except Exception as e:
                failed.append({
                    "company_name": company['company_name'],
                    "email": company['email'],
                    "error": str(e)
                })

        try:
            server.quit()
        except Exception:
            # Ignore quit errors
            pass

        return jsonify({
            "sent": sent,
            "failed": failed,
            "skipped": [{"company_name": c["company_name"], "email": c["email"]} for c in skipped]
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


