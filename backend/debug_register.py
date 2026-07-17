"""
debug_register.py
Tests the full registration flow directly against Google Sheets.
Run from backend folder: python debug_register.py
"""
import os, sys
from dotenv import load_dotenv
load_dotenv()

SHEET_ID     = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL", "")
PRIVATE_KEY  = os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

print("=" * 60)
print("STEP 1: Test Google Sheets Connection")
print("=" * 60)

try:
    import gspread
    from google.oauth2.service_account import Credentials

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

    creds  = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    print("✅ Credentials OK")

    spreadsheet = client.open_by_key(SHEET_ID)
    print(f"✅ Spreadsheet opened: {spreadsheet.title}")

    # List all worksheets
    sheets = spreadsheet.worksheets()
    print(f"✅ Worksheets found: {[s.title for s in sheets]}")

except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
    print("\nFix: Make sure you shared the sheet with:")
    print(f"  {CLIENT_EMAIL}")
    sys.exit(1)

print("\n" + "=" * 60)
print("STEP 2: Get or Create 'Users' Worksheet")
print("=" * 60)

try:
    try:
        ws = spreadsheet.worksheet("Users")
        print("✅ 'Users' tab already exists")
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title="Users", rows=1000, cols=11)
        print("✅ Created new 'Users' tab")

    existing = ws.get_all_values()
    if not existing:
        HEADERS = ["user_id","full_name","email","mobile_number",
                   "branch","college_name","graduation_year","state",
                   "hashed_password","role","created_at"]
        ws.append_row(HEADERS)
        print("✅ Header row added")
    else:
        print(f"✅ Sheet has {len(existing)} rows (including header)")

except Exception as e:
    print(f"❌ WORKSHEET ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("STEP 3: Write a Test Registration Row")
print("=" * 60)

try:
    from datetime import datetime
    test_row = [
        "NXG-DEBUGTEST",
        "Debug User",
        "debug@nexgenu.com",
        "+91 99999 00000",
        "Computer Science Engineering (CSE)",
        "Test College",
        "2026",
        "Tamil Nadu",
        "hashed_pass_placeholder",
        "user",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]
    ws.append_row(test_row)
    print("✅ Test row written successfully!")
    print("   Check your Google Sheet 'Users' tab now.")

except Exception as e:
    print(f"❌ WRITE FAILED: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("STEP 4: Test sheets_db module directly")
print("=" * 60)

try:
    from sheets_db import create_user, get_user_by_email
    found = get_user_by_email("debug@nexgenu.com")
    if found:
        print(f"✅ sheets_db.get_user_by_email works! Found: {found['full_name']}")
    else:
        print("⚠️  Row written but get_user_by_email returned None (check email match)")
except Exception as e:
    print(f"❌ sheets_db import error: {e}")

print("\n" + "=" * 60)
print("ALL DONE. If all steps show ✅, restart the backend and test registration.")
print("=" * 60)
