import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
CLIENT_EMAIL = os.getenv('GOOGLE_CLIENT_EMAIL', '')
PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

print("--- Google Sheets Connection Test ---")
print(f"Sheet ID: {SHEET_ID}")
print(f"Client Email: {CLIENT_EMAIL}")

try:
    creds_info = {
        'type': 'service_account',
        'project_id': 'nexgenu',
        'private_key_id': 'key1',
        'private_key': PRIVATE_KEY,
        'client_email': CLIENT_EMAIL,
        'token_uri': 'https://oauth2.googleapis.com/token',
    }
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    print("\n[1/3] Authenticated with Google successfully!")
    
    sheet = client.open_by_key(SHEET_ID)
    print(f"[2/3] Connected to Spreadsheet: '{sheet.title}' successfully!")
    
    try:
        ws = sheet.worksheet('Users')
        print(f"[3/3] 'Users' worksheet found! It currently has {len(ws.get_all_values())} rows.")
    except Exception as e:
        print(f"[3/3] Could not find 'Users' worksheet. Attempting to create one...")
        ws = sheet.add_worksheet(title="Users", rows=1000, cols=11)
        print("      Created new 'Users' worksheet successfully!")
        
    print("\n✅ All Google Sheets checks passed. Registration should work perfectly.")
        
except Exception as e:
    print(f"\n❌ ERROR CONNECTING TO GOOGLE SHEETS:")
    print(str(e))
    print("\nTroubleshooting Steps:")
    print("1. Ensure you have shared your Google Sheet with this email as an EDITOR:")
    print("   " + CLIENT_EMAIL)
    print("2. Ensure the GOOGLE_SHEET_ID in your .env file is correct.")
