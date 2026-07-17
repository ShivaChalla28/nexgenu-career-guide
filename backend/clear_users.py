"""
clear_users.py
Deletes all user rows from the Google Sheet (keeps header row).
Run from backend folder: python clear_users.py
"""
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

SHEET_ID     = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL", "")
PRIVATE_KEY  = os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

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

print("Connecting to Google Sheets...")
creds  = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_ID)

# Try Users tab first, fall back to sheet1
try:
    ws = spreadsheet.worksheet("Users")
    print("Found 'Users' tab.")
except gspread.WorksheetNotFound:
    ws = spreadsheet.sheet1
    print("Using Sheet1.")

all_rows = ws.get_all_values()
total = len(all_rows)

if total <= 1:
    print("Sheet is already empty (only header row or no data). Nothing to delete.")
else:
    data_rows = total - 1  # exclude header
    print(f"Found {data_rows} registration(s). Clearing...")

    # Clear everything below row 1 (header)
    # Keep header, delete rows 2 onwards
    ws.delete_rows(2, total)

    print(f"✅ Done! Deleted {data_rows} registration(s). Header row kept.")
    print("The sheet is now clean and ready for new registrations.")
