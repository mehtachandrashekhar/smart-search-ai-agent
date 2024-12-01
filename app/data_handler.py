import pandas as pd
import os
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
import json
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_google_credentials():
    credentials_json = st.secrets["environment"]["GOOGLE_CREDENTIALS_JSON"]
    credentials_info = json.loads(credentials_json)
    credentials = Credentials.from_service_account_info(credentials_info)
    return credentials

def handle_csv_upload(uploaded_file):
    """Reads and returns a Pandas DataFrame from the uploaded CSV."""
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise

def handle_google_sheets(sheet_url, range_name="'Sheet1'!A1:Z1000", delay=1):
    """Fetches data from Google Sheets using its API."""
    try:
        # Extract the spreadsheet ID from the URL
        sheet_id = sheet_url.split("/")[5]

        # Load credentials from environment variable
        creds = get_google_credentials()

        # Rate limit compliance
        time.sleep(delay)

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
        values = result.get("values", [])

        if not values:
            logger.warning(f"No data found in the range {range_name} of the Google Sheet.")
            return pd.DataFrame()

        logger.info(f"Fetched {len(values) - 1} rows and {len(values[0])} columns from the Google Sheet.")
        return pd.DataFrame(values[1:], columns=values[0])
    except HttpError as e:
        logger.error(f"Google Sheets API error for sheet {sheet_url}, range {range_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching data from Google Sheets for sheet {sheet_url}, range {range_name}: {e}")
        raise
