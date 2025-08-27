import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Any

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Configure CORS for local dev (adjust origins for production)
    CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000", "*"]}})

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
        emails: List[str] = data.get("emails") or []
        subject: str = (data.get("subject") or "").strip()
        message_html: str = data.get("message") or ""

        if not emails or not subject or not message_html:
            return (
                jsonify({
                    "error": "Missing required fields",
                    "details": {
                        "emails": bool(emails),
                        "subject": bool(subject),
                        "message": bool(message_html),
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

        sent: List[str] = []
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

        # Compose and send per recipient to avoid exposing addresses
        for recipient in emails:
            try:
                msg = MIMEMultipart('alternative')
                msg['From'] = gmail_user
                msg['To'] = recipient
                msg['Subject'] = subject

                # HTML part
                html_part = MIMEText(message_html, 'html')
                msg.attach(html_part)

                server.sendmail(gmail_user, [recipient], msg.as_string())
                sent.append(recipient)
            except Exception as e:
                failed.append({"email": recipient, "error": str(e)})

        try:
            server.quit()
        except Exception:
            # Ignore quit errors
            pass

        return jsonify({"sent": sent, "failed": failed})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


