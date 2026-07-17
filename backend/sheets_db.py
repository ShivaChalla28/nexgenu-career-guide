"""
sheets_db.py
Google Sheets as the User Database for NexGenU.

Sheet structure (auto-created):
  Col A: user_id       | Col B: full_name   | Col C: email
  Col D: mobile_number | Col E: branch      | Col F: college_name
  Col G: graduation_year | Col H: state     | Col I: hashed_password
  Col J: role          | Col K: created_at
"""

import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SHEET_ID     = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL", "")
PRIVATE_KEY  = os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADERS = [
    "user_id", "full_name", "email", "mobile_number",
    "branch", "college_name", "graduation_year", "state",
    "hashed_password", "role", "created_at"
]

# Column indices (1-based for gspread)
COL = {h: i + 1 for i, h in enumerate(HEADERS)}


def _get_sheet():
    """Return the 'Users' worksheet, creating it + headers if needed."""
    creds_info = {
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
    creds  = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)

    # Try to get 'Users' tab; create if it doesn't exist
    try:
        ws = spreadsheet.worksheet("Users")
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title="Users", rows=1000, cols=len(HEADERS))

    # Add headers if sheet is empty
    if not ws.get_all_values():
        ws.append_row(HEADERS)

    return ws


def _row_to_dict(row: list) -> dict:
    """Convert a sheet row list to a user dict."""
    padded = row + [""] * (len(HEADERS) - len(row))
    return {h: padded[i] for i, h in enumerate(HEADERS)}


# ─── Public API ────────────────────────────────────────────────────────────────

def get_user_by_email(email: str) -> dict | None:
    """Return user dict if found, else None."""
    try:
        ws = _get_sheet()
        all_rows = ws.get_all_values()[1:]  # skip header
        for row in all_rows:
            if len(row) > 2 and row[2].strip().lower() == email.strip().lower():
                return _row_to_dict(row)
        return None
    except Exception as e:
        print(f"[SHEETS DB] get_user_by_email error: {e}")
        return None


def get_user_by_id(user_id: str) -> dict | None:
    """Return user dict by user_id (NXG-XXXXX), else None."""
    try:
        ws = _get_sheet()
        all_rows = ws.get_all_values()[1:]  # skip header
        for row in all_rows:
            if len(row) > 0 and row[0].strip() == user_id.strip():
                return _row_to_dict(row)
        return None
    except Exception as e:
        print(f"[SHEETS DB] get_user_by_id error: {e}")
        return None


def create_user(user_data: dict) -> dict:
    """Append a new user row and return the user dict."""
    ws = _get_sheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        user_data.get("user_id", ""),
        user_data.get("full_name", ""),
        user_data.get("email", ""),
        user_data.get("mobile_number", ""),
        user_data.get("branch", ""),
        user_data.get("college_name", ""),
        user_data.get("graduation_year", ""),
        user_data.get("state", ""),
        user_data.get("hashed_password", ""),
        user_data.get("role", "user"),
        now,
    ]
    ws.append_row(row)
    print(f"[SHEETS DB] Created user: {user_data.get('email')}")
    return _row_to_dict(row)


def get_all_users() -> list[dict]:
    """Return all users as a list of dicts (for admin panel)."""
    try:
        ws = _get_sheet()
        all_rows = ws.get_all_values()[1:]  # skip header
        return [_row_to_dict(r) for r in all_rows if r and r[0]]
    except Exception as e:
        print(f"[SHEETS DB] get_all_users error: {e}")
        return []
