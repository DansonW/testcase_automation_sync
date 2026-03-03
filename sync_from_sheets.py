import os
import sys
import csv
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration Helper (Sync with upload_to_sheets.py)
def load_env():
    """Loads environment variables from a .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    # Support both key=value and key = value formats
                    parts = line.strip().split('=', 1)
                    if len(parts) == 2:
                        key, value = parts
                        os.environ[key.strip()] = value.strip()

load_env()

# Get configurations from environment variables
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'service_account/google_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

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

def get_sheet_data(service, spreadsheet_id, sheet_title):
    """Fetches all values from a specific sheet."""
    try:
        # Read the entire sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_title}'!A1:Z"  # Assuming data is within A to Z columns
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print(f"Warning: No data found in sheet '{sheet_title}'.")
        return values
        
    except HttpError as err:
        if "range not found" in str(err).lower():
            print(f"Error: Sheet '{sheet_title}' not found in the spreadsheet.")
        else:
            print(f"An error occurred while fetching data: {err}")
        sys.exit(1)

def write_csv(file_path, data):
    """Writes data to a CSV file with proper formatting."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        # Use csv.QUOTE_MINIMAL or QUOTE_ALL to ensure fields are wrapped if needed
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)
    print(f"Successfully synced data from Google Sheets to '{file_path}'.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sync_from_sheets.py <path_to_local_csv_file>")
        print("Example: python3 sync_from_sheets.py generated_test_cases/Project_A/test_case_20260303_153000.csv")
        sys.exit(1)
        
    csv_file_path = sys.argv[1]
    
    # Generate sheet title from filename (matching the logic in upload_to_sheets.py)
    filename = os.path.basename(csv_file_path)
    sheet_title = os.path.splitext(filename)[0][:100]
    
    print(f"Syncing from Google Sheet: '{sheet_title}' -> Local file: '{csv_file_path}'")
    
    creds = authenticate()
    service = build('sheets', 'v4', credentials=creds)
    
    # 1. Fetch data from Google Sheets
    data = get_sheet_data(service, SPREADSHEET_ID, sheet_title)
    
    # 2. Write data back to local CSV
    if data:
        write_csv(csv_file_path, data)
    else:
        print("Sync aborted because no data was found.")

if __name__ == '__main__':
    main()
