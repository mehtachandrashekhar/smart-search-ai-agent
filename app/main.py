import streamlit as st
import sys
import os
import pandas as pd

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

# Session state initialization
if "data" not in st.session_state:
    st.session_state.data = None

# Handle file or sheet input
data = None
if input_type == "CSV Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        try:
            data = handle_csv_upload(uploaded_file)
            st.write("Uploaded Data Preview:")
            st.dataframe(data)
            st.session_state.data = data  # Store data in session state
        except Exception as e:
            st.error(f"Failed to load CSV: {e}")
elif input_type == "Google Sheets":
    google_sheet_url = st.sidebar.text_input("Enter Google Sheets URL:")
    if google_sheet_url:
        try:
            data = handle_google_sheets(google_sheet_url)
            st.write("Google Sheets Data Preview:")
            st.dataframe(data)
            st.session_state.data = data  # Store data in session state
        except Exception as e:
            st.error(f"Failed to load Google Sheet: {e}")

# Query input and data processing
if st.session_state.data is not None:
    data = st.session_state.data
    selected_column = st.selectbox("Select Column for Entities", data.columns)
    prompt = st.text_area("Enter Query (Use {placeholder} for entity)", "Find the email of {entity}")

    if st.button("Process Data"):
        with st.spinner("Processing data..."):
            results = []
            try:
                for entity in data[selected_column]:
                    # Process the query with the entity
                    formatted_query = process_query(prompt, entity)

                    # Perform web search and extract information
                    search_results = perform_search(formatted_query)
                    extracted_info = extract_information(search_results, formatted_query)

                    # Append results
                    results.append({"Entity": entity, "Result": extracted_info})

                # Display results in the app
                st.success("Data processing complete!")
                st.write("Results:")
                st.dataframe(results)

                # Convert results to DataFrame for CSV download
                results_df = pd.DataFrame(results)

                # Download results as a CSV file
                st.download_button(
                    "Download Results as CSV",
                    data=results_df.to_csv(index=False),
                    file_name="results.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error during processing: {e}")
else:
    st.info("Please upload a CSV or provide a Google Sheets URL to begin.")
