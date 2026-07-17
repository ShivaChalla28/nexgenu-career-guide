import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
CLIENT_EMAIL = os.getenv('GOOGLE_CLIENT_EMAIL', '')
PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
HEADERS = [
    "user_id", "full_name", "email", "mobile_number",
    "branch", "college_name", "graduation_year", "state",
    "hashed_password", "role", "created_at"
]

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
    
    # Check if headers already exist in the first row
    first_row = ws.row_values(1)
    if first_row and first_row[0] == "user_id":
        print("Headers already exist!")
    else:
        # Insert a new row at the very top (index 1)
        print("Inserting headers at the top of the sheet...")
        ws.insert_row(HEADERS, index=1)
        
        # Apply some basic formatting to make the headers bold
        ws.format("A1:K1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
        })
        print("✅ Headers successfully added and formatted!")
        
except Exception as e:
    print("Error:", str(e))
