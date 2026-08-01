"""
sheets_db.py
Google Sheets as the User Database for NexGenU.

Sheet structure (auto-created):
  Col A: user_id       | Col B: full_name   | Col C: email
  ... and now supports many other collections.
"""

import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

SHEET_ID     = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL", "")
PRIVATE_KEY  = os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# We define schemas for each collection
SCHEMAS = {
    "Users": ["user_id", "full_name", "email", "mobile_number", "branch", "college_name", "graduation_year", "state", "hashed_password", "role", "created_at"],
    "Jobs": ["job_id", "title", "company", "location", "type", "description", "requirements", "status", "recruiter_id", "created_at"],
    "Internships": ["internship_id", "title", "company", "location", "duration", "stipend", "description", "requirements", "status", "recruiter_id", "created_at"],
    "Applications": ["app_id", "user_id", "job_id", "type", "status", "resume_link", "applied_at"],
    "Hackathons": ["hackathon_id", "title", "description", "start_date", "end_date", "team_size", "fee", "status", "created_at"],
    "Teams": ["team_id", "hackathon_id", "name", "leader_id", "members", "project_link", "status", "created_at"],
    "StartupIdeas": ["idea_id", "user_id", "title", "description", "pitch_deck", "mentor_id", "status", "feedback", "created_at"],
    "Settings": ["key", "value", "updated_at"],
    "Pricing": ["plan_id", "name", "price", "features", "role"],
    "Payments": ["payment_id", "user_id", "amount", "status", "purpose", "reference_id", "created_at"]
}

@lru_cache(maxsize=1)
def _get_client():
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
    return gspread.authorize(creds)

def _get_sheet(sheet_name: str):
    client = _get_client()
    spreadsheet = client.open_by_key(SHEET_ID)
    headers = SCHEMAS.get(sheet_name, [])
    
    try:
        ws = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=max(len(headers), 1))
    
    if headers and not ws.get_all_values():
        ws.append_row(headers)
    
    return ws

def _row_to_dict(row: list, sheet_name: str) -> dict:
    headers = SCHEMAS.get(sheet_name, [])
    padded = row + [""] * (len(headers) - len(row))
    return {h: padded[i] for i, h in enumerate(headers)}


# ─── Generic CRUD API ─────────────────────────────────────────────────────────

def get_all(sheet_name: str) -> list[dict]:
    try:
        ws = _get_sheet(sheet_name)
        all_rows = ws.get_all_values()
        if not all_rows or len(all_rows) < 2: return []
        return [_row_to_dict(r, sheet_name) for r in all_rows[1:] if r and r[0]]
    except Exception as e:
        print(f"[SHEETS DB] get_all error for {sheet_name}: {e}")
        return []

def get_by_id(sheet_name: str, id_col_idx: int, item_id: str) -> dict | None:
    try:
        ws = _get_sheet(sheet_name)
        all_rows = ws.get_all_values()
        if not all_rows or len(all_rows) < 2: return None
        for row in all_rows[1:]:
            if len(row) > id_col_idx and row[id_col_idx].strip() == item_id.strip():
                return _row_to_dict(row, sheet_name)
        return None
    except Exception as e:
        print(f"[SHEETS DB] get_by_id error for {sheet_name}: {e}")
        return None

def create_item(sheet_name: str, item_data: dict) -> dict:
    ws = _get_sheet(sheet_name)
    headers = SCHEMAS.get(sheet_name, [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "created_at" in headers and not item_data.get("created_at"):
        item_data["created_at"] = now
    
    row = [str(item_data.get(h, "")) for h in headers]
    ws.append_row(row)
    print(f"[SHEETS DB] Created {sheet_name} entry: {item_data.get(headers[0], 'N/A')}")
    return _row_to_dict(row, sheet_name)

def update_item(sheet_name: str, id_col_idx: int, item_id: str, updates: dict) -> dict | None:
    try:
        ws = _get_sheet(sheet_name)
        all_rows = ws.get_all_values()
        if not all_rows or len(all_rows) < 2: return None
        headers = SCHEMAS.get(sheet_name, [])
        for i, row in enumerate(all_rows):
            if i == 0: continue
            if len(row) > id_col_idx and row[id_col_idx].strip() == item_id.strip():
                current_dict = _row_to_dict(row, sheet_name)
                current_dict.update(updates)
                if "updated_at" in headers:
                    current_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [str(current_dict.get(h, "")) for h in headers]
                # Update the row in sheets (i+1 is the row number)
                ws.update(f"A{i+1}", [new_row])
                print(f"[SHEETS DB] Updated {sheet_name} entry: {item_id}")
                return current_dict
        return None
    except Exception as e:
        print(f"[SHEETS DB] update_item error for {sheet_name}: {e}")
        return None

def delete_item(sheet_name: str, id_col_idx: int, item_id: str) -> bool:
    try:
        ws = _get_sheet(sheet_name)
        all_rows = ws.get_all_values()
        if not all_rows or len(all_rows) < 2: return False
        for i, row in enumerate(all_rows):
            if i == 0: continue
            if len(row) > id_col_idx and row[id_col_idx].strip() == item_id.strip():
                ws.delete_rows(i + 1)
                print(f"[SHEETS DB] Deleted {sheet_name} entry: {item_id}")
                return True
        return False
    except Exception as e:
        print(f"[SHEETS DB] delete_item error for {sheet_name}: {e}")
        return False


# ─── Users Specific API (Backward Compatibility) ──────────────────────────────

def get_user_by_email(email: str) -> dict | None:
    try:
        ws = _get_sheet("Users")
        all_rows = ws.get_all_values()[1:]
        for row in all_rows:
            if len(row) > 2 and row[2].strip().lower() == email.strip().lower():
                return _row_to_dict(row, "Users")
        return None
    except Exception as e:
        print(f"[SHEETS DB] get_user_by_email error: {e}")
        return None

def get_user_by_id(user_id: str) -> dict | None:
    return get_by_id("Users", 0, user_id)

def create_user(user_data: dict) -> dict:
    return create_item("Users", user_data)

def get_all_users() -> list[dict]:
    return get_all("Users")
