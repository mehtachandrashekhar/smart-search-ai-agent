import streamlit as st
import sys
import os
from dotenv import load_dotenv
import pandas as pd
import hvac
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Vault client
client = hvac.Client(url='http://127.0.0.1:8200')
client.token = os.getenv('VAULT_TOKEN')  # Ensure you have the VAULT_TOKEN set in your environment

# Fetch secrets from Vault
api_keys_secret = client.secrets.kv.v2.read_secret_version(path='api_keys')
settings_secret = client.secrets.kv.v2.read_secret_version(path='settings')
secrets_secret = client.secrets.kv.v2.read_secret_version(path='secrets')
environment_secret = client.secrets.kv.v2.read_secret_version(path='environment')
connections_gsheets_secret = client.secrets.kv.v2.read_secret_version(path='connections/gsheets')

# Set environment variables
os.environ['GOOGLE_SHEETS_API_KEY'] = api_keys_secret['data']['data']['google_sheets']
os.environ['WEB_SCRAPER_API_KEY'] = api_keys_secret['data']['data']['web_scraper']
os.environ['LLM_API_KEY'] = api_keys_secret['data']['data']['llm_api']
os.environ['RATE_LIMIT'] = settings_secret['data']['data']['rate_limit']
os.environ['SERPAPI_KEY'] = secrets_secret['data']['data']['SERPAPI_KEY']
os.environ['GROQ_API_KEY'] = secrets_secret['data']['data']['GROQ_API_KEY']
os.environ['GROQ_API_URL'] = secrets_secret['data']['data']['GROQ_API_URL']
os.environ['GROQ_MODEL'] = secrets_secret['data']['data']['GROQ_MODEL']
os.environ['GROQ_MAX_TOKENS'] = secrets_secret['data']['data']['GROQ_MAX_TOKENS']
os.environ['GROQ_CONTEXT_MAX_TOKENS'] = secrets_secret['data']['data']['GROQ_CONTEXT_MAX_TOKENS']
os.environ['GOOGLE_CREDENTIALS_JSON'] = environment_secret['data']['data']['GOOGLE_CREDENTIALS_JSON']
os.environ['GOOGLE_SHEETS_URL'] = connections_gsheets_secret['data']['data']['spreadsheet']

# Parse the Google credentials JSON string
google_credentials_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])

# Debugging: Print sys.path and working directory
# st.write(sys.path)
# st.write("Current Working Directory:", os.getcwd())

# Ensure the project root is added to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
from app.data_handler import handle_csv_upload, handle_google_sheets
from app.query_processor import process_query
from app.web_scraper import perform_search
from app.llm_integration import extract_information

# Streamlit app title
st.title("AI Agent for Data Processing")

# Sidebar for file upload or Google Sheets input
st.sidebar.header("Data Input")
input_type = st.sidebar.selectbox("Select Input Type", ["CSV Upload", "Google Sheets"])

if input_type == "CSV Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        # Handle CSV upload
        data = handle_csv_upload(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.write(data)
        st.session_state.data = data  # Store data in session state
elif input_type == "Google Sheets":
    google_sheet_url = st.sidebar.text_input("Enter Google Sheets URL:", value=os.getenv('GOOGLE_SHEETS_URL'))
    if google_sheet_url:
        # Handle Google Sheets input
        data = handle_google_sheets(google_sheet_url)
        st.write("Google Sheets Data Preview:")
        st.write(data)
        st.session_state.data = data  # Store data in session state

# Query input and data processing
if "data" in st.session_state:
    data = st.session_state.data
    selected_column = st.selectbox("Select Column for Entities", data.columns)
    prompt = st.text_area("Enter Query (Use {placeholder} for entity)", "Find the email of {entity}")

    if st.button("Process Data"):
        results = []
        for entity in data[selected_column]:
            # Process the query with the entity
            formatted_query = process_query(prompt, entity)

            # Perform web search and extract information
            search_results = perform_search(formatted_query)
            extracted_info = extract_information(search_results, formatted_query)

            # Append results
            results.append({"Entity": entity, "Result": extracted_info})

        # Display results in the app
        st.write("Results:")
        st.write(results)

        # Convert results to DataFrame for CSV download
        results_df = pd.DataFrame(results)

        # Download results as a CSV file
        st.download_button(
            "Download Results as CSV",
            data=results_df.to_csv(index=False),
            file_name="results.csv",
            mime="text/csv"
        )
