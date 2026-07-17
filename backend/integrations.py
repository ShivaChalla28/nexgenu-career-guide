"""
integrations.py
Handles:
  1. Welcome email via Gmail SMTP
  2. Google Sheets user registration sync
"""

import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── Config ───────────────────────────────────────────────────────────────────
EMAIL_HOST  = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT  = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER  = os.getenv("EMAIL_USER", "")
EMAIL_PASS  = os.getenv("EMAIL_PASS", "")

SHEET_ID         = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_EMAIL     = os.getenv("GOOGLE_CLIENT_EMAIL", "")
PRIVATE_KEY_RAW  = os.getenv("GOOGLE_PRIVATE_KEY", "")

# Fix escaped newlines from .env
PRIVATE_KEY = PRIVATE_KEY_RAW.replace("\\n", "\n")


# ─── 1. Welcome Email ─────────────────────────────────────────────────────────
def send_welcome_email(to_email: str, full_name: str, user_id: str, branch: str):
    """Send a branded HTML welcome email to the new user."""
    try:
        subject = "🎉 Welcome to NexGenU – Your Career Journey Starts Now!"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f0f; color: #e5e5e5; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 40px auto; background: #1a1a2e; border-radius: 16px; overflow: hidden; border: 1px solid #2d2d4e; }}
    .header {{ background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899); padding: 40px 32px; text-align: center; }}
    .header h1 {{ margin: 0; color: white; font-size: 32px; font-weight: 900; letter-spacing: -1px; }}
    .header p {{ color: rgba(255,255,255,0.8); margin: 8px 0 0; font-size: 14px; }}
    .body {{ padding: 36px 32px; }}
    .greeting {{ font-size: 22px; font-weight: 700; margin-bottom: 12px; color: #f1f5f9; }}
    .text {{ color: #94a3b8; line-height: 1.7; font-size: 15px; margin-bottom: 20px; }}
    .card {{ background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 20px 24px; margin: 24px 0; }}
    .card-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #64748b; margin-bottom: 4px; }}
    .card-value {{ font-size: 16px; font-weight: 700; color: #e2e8f0; }}
    .badge {{ display: inline-block; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; font-size: 20px; font-weight: 900; padding: 10px 24px; border-radius: 8px; letter-spacing: 2px; font-family: monospace; }}
    .cta {{ text-align: center; margin: 32px 0; }}
    .cta a {{ display: inline-block; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; text-decoration: none; font-weight: 700; font-size: 16px; padding: 16px 40px; border-radius: 50px; }}
    .steps {{ margin: 24px 0; }}
    .step {{ display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px; }}
    .step-num {{ width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; font-weight: 900; font-size: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
    .step-text {{ color: #94a3b8; font-size: 14px; line-height: 1.5; padding-top: 6px; }}
    .footer {{ background: #0f0f0f; padding: 24px 32px; text-align: center; border-top: 1px solid #1e293b; }}
    .footer p {{ color: #475569; font-size: 12px; margin: 4px 0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>NexGenU</h1>
      <p>Career Vision Roadmaps • India's Engineering Career Platform</p>
    </div>
    <div class="body">
      <div class="greeting">Hello, {full_name}! 👋</div>
      <p class="text">
        Welcome to <strong>NexGenU</strong> — India's most comprehensive engineering career platform.
        Your account has been successfully created. Here are your details:
      </p>

      <div class="card">
        <div class="card-label">Your Unique User ID</div>
        <div class="badge">{user_id}</div>
        <div style="margin-top:12px">
          <div class="card-label">Registered Branch</div>
          <div class="card-value">{branch}</div>
        </div>
      </div>

      <p class="text">
        Save your <strong>User ID</strong> — you can use it to log in anytime instead of your email.
      </p>

      <p class="text"><strong>Here's how to get started:</strong></p>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <div class="step-text">Login with your email or User ID and explore your personalized dashboard.</div>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <div class="step-text">Go to your branch page and explore Core, IT & Digital, and Government & PSU career paths.</div>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <div class="step-text">Pick a career, follow the roadmap, and start building your future today.</div>
        </div>
      </div>

      <div class="cta">
        <a href="https://engineeeringroadmaps.nexgenu.dpdns.org/auth/login">Go to My Dashboard →</a>
      </div>

      <p class="text" style="font-size:13px; text-align:center;">
        Need help? Join our WhatsApp community or reply to this email.<br/>
        We're here to guide you every step of the way. 🚀
      </p>
    </div>
    <div class="footer">
      <p><strong>NexGenU Career Vision Roadmaps</strong></p>
      <p>India's #1 Engineering Career Platform</p>
      <p style="margin-top:8px; color:#334155;">© {datetime.now().year} NexGenU. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"NexGenU Careers <{EMAIL_USER}>"
        msg["To"]      = to_email

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"[EMAIL] Welcome email sent to {to_email}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send to {to_email}: {e}")


# ─── 2. Google Sheets Sync ────────────────────────────────────────────────────
def sync_to_google_sheets(user_data: dict):
    """Append a new user row to the Google Sheet."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials_info = {
            "type": "service_account",
            "project_id": "nexgenu",
            "private_key_id": "key1",
            "private_key": PRIVATE_KEY,
            "client_email": CLIENT_EMAIL,
            "client_id": "",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{CLIENT_EMAIL}",
        }

        creds  = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(SHEET_ID).sheet1

        # Add header row if sheet is empty
        if sheet.row_count == 0 or not sheet.get_all_values():
            sheet.append_row([
                "Timestamp", "User ID", "Full Name", "Email",
                "Mobile", "Branch", "College", "Graduation Year", "State"
            ])

        # Append user data
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_data.get("user_id", ""),
            user_data.get("full_name", ""),
            user_data.get("email", ""),
            user_data.get("mobile_number", ""),
            user_data.get("branch", ""),
            user_data.get("college_name", ""),
            user_data.get("graduation_year", ""),
            user_data.get("state", ""),
        ])

        print(f"[SHEETS] Synced user {user_data.get('user_id')} to Google Sheets")

    except ImportError:
        print("[SHEETS ERROR] gspread / google-auth not installed. Run: pip install gspread google-auth")
    except Exception as e:
        print(f"[SHEETS ERROR] Failed to sync {user_data.get('email')}: {e}")
