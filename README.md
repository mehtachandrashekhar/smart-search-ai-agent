# Smart Search AI Agent

## Overview

The **Smart Search AI Agent** is a powerful Streamlit application designed to streamline data processing. It allows users to upload CSV files or connect to Google Sheets, perform web searches for relevant information, and extract structured data using advanced language models. This tool is particularly useful for automating information retrieval and enhancing productivity.

---

## Features

- **Data Integration**:
  - Upload CSV files or link Google Sheets for processing.
  - Preview and select specific columns for data processing.
- **Dynamic Querying**:
  - Create custom queries using placeholders like `{entity}`.
  - Automatically insert data from the selected column into queries.
- **Automated Web Search**:
  - Perform searches using APIs like SerpAPI and gather structured results.
- **LLM Integration**:
  - Use OpenAI GPT or Groq LLM to extract precise information from search results.
- **Results Display and Export**:
  - View extracted data directly in the app and download it as a CSV file.

---

## Prerequisites

Before starting, ensure you have the following:

- **Python 3.10 or later**
- **Git**
- API Keys for:
  - [Google Sheets](https://console.cloud.google.com/)
  - [SerpAPI](https://serpapi.com/)
  - [OpenAI](https://platform.openai.com/)
  - [Groq AI](https://groq.com/)

---

## Setup

### Step 1: Clone the Repository

Clone the project to your local machine:

```sh
git clone https://github.com/mehtachandrashekhar/smart-search-ai-agent.git
cd smart-search-ai-agent
```

### Step 2: Create a Virtual Environment

Set up a virtual environment for managing dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root to store sensitive API keys:

```plaintext
SERPAPI_KEY=your_serpapi_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CREDENTIALS_PATH=config/credentials.json
GROQ_API_KEY=your_groq_api_key
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=llama3-8b-8192
GROQ_MAX_TOKENS=100
GROQ_CONTEXT_MAX_TOKENS=4096
```

### Step 5: Create Configuration Files

1. **`config/credentials.json`**: Configure your Google Sheets service account:
   ```json
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-private-key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\nyour-private-key\n-----END PRIVATE KEY-----\n",
     "client_email": "your-client-email",
     "client_id": "your-client-id",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-client-email"
   }
   ```

2. **`config/config.yaml`**: Store API keys and settings:
   ```yaml
   api:
     serpapi_key: your_serpapi_key
     openai_api_key: your_openai_api_key
     google_credentials_path: config/credentials.json
     groq_api_key: your_groq_api_key
     groq_api_url: https://api.groq.com/openai/v1/chat/completions
     groq_model: llama3-8b-8192
     groq_max_tokens: 100
     groq_context_max_tokens: 4096
   ```

### Step 6: Share Google Sheets with Service Account

1. Open the Google Sheet you want to process.
2. Click on the **"Share"** button.
3. Add the **service account email** from `credentials.json`.
4. Set permissions to **Editor** and save.

### Step 7: Update `.gitignore`

Ensure sensitive files are ignored by Git:

```plaintext
# Environment variables
.env

# Configuration files
config/
```

### Step 8: Run the Application

Start the Streamlit app:

```sh
streamlit run app/main.py
```

---

## Usage

1. **Upload CSV/Connect Google Sheets**:
   - Use the sidebar to upload a CSV file or enter a Google Sheets URL.
2. **Select Column**:
   - Choose the column containing entities for processing.
3. **Enter Query**:
   - Input a query with placeholders (e.g., `Find the email of {entity}`).
4. **Process Data**:
   - Click **"Process Data"** to search and extract results.
5. **View and Export**:
   - View the extracted results in the app and download them as a CSV file.

---

## Contribution

Contributions are always welcome! Here’s how you can contribute:

1. **Fork the Repository**:
   - Click the "Fork" button on GitHub.
2. **Create a Branch**:
   - Create a branch for your feature or bug fix:
     ```sh
     git checkout -b feature-name
     ```
3. **Make Changes**:
   - Add your feature or fix the bug.
4. **Push to GitHub**:
   - Push your branch:
     ```sh
     git push origin feature-name
     ```
5. **Submit a Pull Request**:
   - Open a pull request on the original repository.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
