# Cold Email Sender (Flask + Vanilla JS)

A simple cold email sender web app.

- Frontend: HTML, CSS, JavaScript (no framework)
- Backend: Flask (Python)
- Email: Gmail SMTP (App Password)

## Project Structure

```
backend/
  app.py
  requirements.txt
  static/
    style.css
    script.js
  templates/
    index.html
```

## Prerequisites

- Python 3.10+
- Gmail account with 2‑Step Verification enabled
- Gmail App Password created for "Mail"

## Setup: Backend

1. Open a terminal in the `backend` folder.
2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# or CMD
.venv\\Scripts\\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables (required):

- `GMAIL_USER`: your Gmail address (e.g. `you@gmail.com`)
- `GMAIL_APP_PASSWORD`: your 16-character app password

Windows PowerShell example:

```powershell
$env:GMAIL_USER = "you@gmail.com"
$env:GMAIL_APP_PASSWORD = "abcd efgh ijkl mnop"  # no spaces also works
python app.py
```

macOS/Linux example:

```bash
export GMAIL_USER="you@gmail.com"
export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"
python app.py
```

This starts the API at `http://127.0.0.1:5000`.

## Frontend

Served by Flask at `/`. Open `http://127.0.0.1:5000/` after starting the backend.

## Usage

1. Start the backend (`python backend/app.py`).
2. Open `http://127.0.0.1:5000/`.
3. Paste comma-separated emails, enter subject and HTML message.
4. Click "Send Emails". The result panel will show sent/failed counts and details.

## Notes & Error Handling

- The backend sends each email individually to avoid exposing recipient lists.
- If SMTP login fails (wrong app password, 2FA not enabled), the API returns 502 with details.
- The response includes `sent` and `failed` arrays. Failures contain the target `email` and the error string.
- CORS is enabled for typical localhost ports. Adjust in `backend/app.py` for production.

## Security Considerations

- Never commit real credentials. Use environment variables or secret managers.
- Gmail has sending limits; avoid spamming. Ensure compliance with email laws (CAN-SPAM/GDPR, etc.).
- Prefer a dedicated sending domain and service for production-scale cold outreach.

## License

MIT


