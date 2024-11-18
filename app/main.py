import streamlit as st
import sys
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

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
    google_sheet_url = st.sidebar.text_input("Enter Google Sheets URL:")
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
