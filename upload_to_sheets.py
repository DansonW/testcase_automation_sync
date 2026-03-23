import os
import sys
import csv
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import validate_csv

# Configuration Helper
def load_env():
    """Loads environment variables from a .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# Get configurations from environment variables
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'service_account/google_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    """Authenticates using the service account file."""
    if not SPREADSHEET_ID:
        print("Error: SPREADSHEET_ID environment variable not set. Please check your .env file.")
        sys.exit(1)
        
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: Credentials file not found at {CREDENTIALS_FILE}. Please check your .env file or place the JSON file correctly.")
        sys.exit(1)
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return creds

def read_csv(file_path):
    """Reads the CSV file and returns data as a list of lists."""
    if not os.path.exists(file_path):
        print(f"Error: CSV file '{file_path}' not found.")
        sys.exit(1)
        
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

def upload_to_sheet(service, spreadsheet_id, sheet_title, data):
    """Creates a new sheet and uploads data to it."""
    try:
        # 1. Add a new sheet
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_title
                    }
                }
            }]
        }
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        
        sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        print(f"Created new sheet '{sheet_title}' (ID: {sheet_id})")
        
        # 2. Write data to the new sheet
        body = {
            'values': data
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_title}'!A1",
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"Successfully uploaded {len(data)} rows to sheet '{sheet_title}'.")
        
    except HttpError as err:
        print(f"An error occurred: {err}")
        # If sheet already exists, maybe append a timestamp or handle it?
        if "already exists" in str(err):
            print(f"Sheet '{sheet_title}' already exists. Skipping creation.")
            # Optional: Implement overwrite logic or append timestamp
        else:
            raise

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_sheets.py <path_to_csv_file> [--cleanup]")
        sys.exit(1)
        
    csv_file_path = sys.argv[1]
    
    # Validation Step
    print(f"Validating {csv_file_path}...")
    if not validate_csv.validate_csv(csv_file_path):
        print("Validation failed. Upload aborted.")
        sys.exit(1)

    cleanup = '--cleanup' in sys.argv
    
    # Generate sheet title from filename (limit length if necessary)
    # Google Sheets title max length is 100 characters.
    filename = os.path.basename(csv_file_path)
    sheet_title = os.path.splitext(filename)[0][:100]
    
    creds = authenticate()
    service = build('sheets', 'v4', credentials=creds)
    
    data = read_csv(csv_file_path)
    upload_to_sheet(service, SPREADSHEET_ID, sheet_title, data)

    if cleanup:
        try:
            os.remove(csv_file_path)
            print(f"Successfully removed temporary file: {csv_file_path}")
        except OSError as e:
            print(f"Error removing file {csv_file_path}: {e}")

if __name__ == '__main__':
    main()
