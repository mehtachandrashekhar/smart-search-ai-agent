from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

def test_google_sheets(sheet_url):
    # Extract the spreadsheet ID from the URL
    sheet_id = sheet_url.split("/")[5]

    # Load credentials
    creds = Credentials.from_service_account_file("config/credentials.json")
    service = build("sheets", "v4", credentials=creds)

    # Fetch data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1").execute()
    values = result.get("values", [])

    # Convert to DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])
    print("Google Sheets Data:")
    print(df)

# Test
test_google_sheets("https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit")
