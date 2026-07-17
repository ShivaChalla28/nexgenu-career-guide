import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
CLIENT_EMAIL = os.getenv('GOOGLE_CLIENT_EMAIL', '')
PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

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
    
    sheet = client.open_by_key(SHEET_ID)
    ws = sheet.worksheet('Users')
    
    print("==================================================")
    print("THE BACKEND IS CURRENTLY WRITING TO THIS GOOGLE SHEET:")
    print(f"Name: {sheet.title}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print("==================================================\n")
    
    rows = ws.get_all_values()
    print(f"Total Rows in the 'Users' tab: {len(rows)}")
    
    for i, row in enumerate(rows):
        print(f"Row {i+1}: {row}")
        
except Exception as e:
    print("Error:", str(e))
