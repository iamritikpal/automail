# 📧 Cold Email Sender

A production-ready cold email sender web application built with Flask and vanilla JavaScript. Features CSV upload, template personalization, resume attachments, and intelligent duplicate prevention.

## 🚀 Features

- **📁 CSV Upload**: Bulk import company data via CSV files
- **🎯 Template Personalization**: Dynamic message templates with `{{company_name}}` placeholders
- **📎 Resume Attachments**: Automatic PDF resume attachment to every email
- **🔄 Duplicate Prevention**: Smart logging prevents sending duplicate emails
- **📊 Real-time Preview**: CSV data preview before sending
- **📈 Detailed Analytics**: Track sent, failed, and skipped emails
- **🔒 Secure**: Gmail SMTP with App Password authentication

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (Browser)     │    │   (Flask)       │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • HTML/CSS/JS   │◄──►│ • Flask App     │◄──►│ • Gmail SMTP    │
│ • CSV Upload    │    │ • CSV Parser    │    │ • App Password  │
│ • Template UI   │    │ • Email Sender  │    │                 │
│ • Preview       │    │ • Resume Attach │    │                 │
│ • Results       │    │ • CSV Logger    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Local Files   │
                       ├─────────────────┤
                       │ • sent_log.csv  │
                       │ • resume.pdf    │
                       │ • .env          │
                       └─────────────────┘
```

## 📁 Project Structure

```
autoemail/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── sample_companies.csv   # Example CSV data
│   ├── sent_log.csv          # Email sending history (auto-generated)
│   ├── static/
│   │   ├── style.css         # Frontend styles
│   │   └── script.js         # Frontend JavaScript
│   ├── templates/
│   │   └── index.html        # Main web interface
│   └── resume/
│       └── my_resume.pdf     # Resume file (user-provided)
└── README.md
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | User interface, CSV upload, preview |
| **Backend** | Flask (Python) | API server, email processing, file handling |
| **Email** | Gmail SMTP | Email delivery with App Password auth |
| **Storage** | Local CSV files | Data persistence and logging |
| **Styling** | Custom CSS | Modern, responsive dark theme |

## ⚙️ Prerequisites

- **Python 3.10+** - Backend runtime
- **Gmail Account** - With 2-Step Verification enabled
- **Gmail App Password** - 16-character password for SMTP access
- **Resume PDF** - Your resume file for attachments

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd autoemail/backend
python -m venv .venv
```

### 2. Activate Environment

**Windows (PowerShell):**
```powershell
. .venv/Scripts/Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the `backend/` directory:

```env
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

**Or set environment variables directly:**

**Windows (PowerShell):**
```powershell
$env:GMAIL_USER = "your.email@gmail.com"
$env:GMAIL_APP_PASSWORD = "your-16-char-app-password"
```

**macOS/Linux:**
```bash
export GMAIL_USER="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your-16-char-app-password"
```

### 5. Add Resume

Place your resume PDF file at:
```
backend/resume/my_resume.pdf
```

### 6. Run Application

```bash
python app.py
```

Open your browser and navigate to: **http://127.0.0.1:5000**

## 📋 Usage Guide

### 1. Prepare Your CSV Data

Create a CSV file with the following structure:

```csv
company_name,email
Acme Corporation,hr@acme.com
TechStart Inc,careers@techstart.com
Innovation Labs,hello@innovationlabs.com
```

**Required Columns:**
- `company_name` - Company name for personalization
- `email` - Recipient email address

### 2. Create Message Template

Use the `{{company_name}}` placeholder in your message:

```html
<p>Hello {{company_name}},</p>
<p>I hope this email finds you well.</p>
<p>I'm reaching out because I'm interested in opportunities at your company.</p>
<p>Best regards,<br>Your Name</p>
```

### 3. Send Emails

1. Upload your CSV file
2. Review the data preview
3. Enter email subject
4. Write your message template
5. Click "Send Emails"

### 4. Monitor Results

The application will show:
- ✅ **Sent**: Successfully delivered emails
- ❌ **Failed**: Emails that couldn't be sent
- ⏭️ **Skipped**: Duplicate emails (already sent before)

## 🔧 Configuration

### Email Settings

The application uses Gmail SMTP with the following settings:
- **Server**: `smtp.gmail.com`
- **Port**: `587`
- **Security**: TLS encryption
- **Authentication**: App Password (not regular password)

### File Paths

| File | Path | Description |
|------|------|-------------|
| Resume | `backend/resume/my_resume.pdf` | Resume attachment |
| Sent Log | `backend/sent_log.csv` | Email history (auto-generated) |
| Sample Data | `backend/sample_companies.csv` | Example CSV file |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_USER` | Yes | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Yes | 16-character app password |

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/health` | GET | Health check endpoint |
| `/send-emails` | POST | Send personalized emails |

### `/send-emails` Request Format

```json
{
  "csv_content": "company_name,email\nAcme Corp,hr@acme.com",
  "subject": "Job Application",
  "message": "<p>Hello {{company_name}},</p>"
}
```

### Response Format

```json
{
  "sent": [
    {"company_name": "Acme Corp", "email": "hr@acme.com"}
  ],
  "failed": [
    {"company_name": "Invalid Corp", "email": "invalid@email", "error": "Invalid email"}
  ],
  "skipped": [
    {"company_name": "Already Sent Corp", "email": "already@sent.com"}
  ]
}
```

## 🛡️ Security Features

- **Environment Variables**: Credentials stored securely
- **App Passwords**: Gmail 2FA with dedicated app password
- **Duplicate Prevention**: Prevents accidental re-sending
- **Individual Sending**: Each email sent separately for privacy
- **Input Validation**: CSV format and email validation

## 🚨 Error Handling

| Error Type | HTTP Code | Description |
|------------|-----------|-------------|
| Missing Fields | 400 | Required CSV, subject, or message missing |
| Invalid CSV | 400 | CSV format or column validation failed |
| SMTP Login Failed | 502 | Gmail authentication failed |
| File Not Found | 500 | Resume file missing |

## 📈 Monitoring & Logging

### Sent Log Format

The `sent_log.csv` file tracks all sent emails:

```csv
company_name,email,timestamp
Acme Corp,hr@acme.com,2024-01-15T10:30:00
TechStart Inc,careers@techstart.com,2024-01-15T10:31:15
```

### Log Analysis

You can analyze your sending history:
- Track successful sends
- Monitor sending patterns
- Identify duplicate attempts
- Export data for reporting

## 🔄 Development

### Local Development

```bash
cd backend
python app.py
```

The application runs in debug mode with auto-reload enabled.

### Production Deployment

For production deployment:

1. **Update CORS settings** in `app.py`
2. **Use environment variables** for credentials
3. **Configure proper logging**
4. **Set up monitoring**
5. **Use HTTPS**

### Customization

- **Resume Path**: Modify `attach_resume()` function
- **Email Template**: Extend `personalize_message()` function
- **Logging**: Customize `log_sent_email()` function
- **Styling**: Update `static/style.css`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Legal & Compliance

- **CAN-SPAM Act**: Ensure compliance with email marketing laws
- **GDPR**: Respect privacy regulations for EU recipients
- **Rate Limits**: Respect Gmail's sending limits
- **Best Practices**: Use for legitimate business communication only

## 🆘 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| SMTP Login Failed | Verify Gmail App Password and 2FA |
| Resume Not Attached | Check file exists at `resume/my_resume.pdf` |
| CSV Upload Error | Ensure CSV has required columns |
| Duplicate Emails | Check `sent_log.csv` for existing entries |

### Getting Help

1. Check the error messages in the browser console
2. Review the Flask application logs
3. Verify your CSV format matches the example
4. Ensure all environment variables are set correctly

---

**Built with ❤️ using Flask and Vanilla JavaScript**


