# Smart Search AI Agent

## Overview

The Smart Search AI Agent is a Streamlit application designed to process data from CSV files or Google Sheets, perform web searches, and extract relevant information using language models. This project includes the use of various API keys for authentication and data processing.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or later
- Git

## Setup

### Step 1: Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/your-username/smart-search-ai-agent.git
cd smart-search-ai-agent
```

### Step 2: Create a Virtual Environment

Create a virtual environment to manage dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory of your project to store your environment variables. Add the following variables to the `.env` file:

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

Create a `config` directory in the root of your project and add your `credentials.json` and `config.yaml` files to this directory.

#### Example: `credentials.json`

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

#### Example: `config.yaml`

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

### Step 6: Share Google Sheet with Service Account

1. **Open Google Sheets**: Go to your Google Sheets document.
2. **Share the Sheet**: Click on the "Share" button in the top-right corner.
3. **Add Service Account Email**: In the "Share with people and groups" dialog, enter the service account email (found in your `credentials.json` file under `client_email`).
4. **Set Permissions**: Set the permissions to "Editor" and click "Send".

### Step 7: Update `.gitignore`

Ensure that your `.gitignore` file includes the `.env` file and the `config` directory to prevent them from being pushed to GitHub:

```plaintext
# Ignore environment variables file
.env

# Ignore config directory
config/
```

### Step 8: Run the Application

Run the Streamlit application:

```sh
streamlit run app/main.py
```

## Usage

1. **Upload a CSV File**: Use the sidebar to upload a CSV file.
2. **Enter Google Sheets URL**: Alternatively, enter the URL of a Google Sheets document.
3. **Select Column for Entities**: Choose the column containing the entities you want to process.
4. **Enter Query**: Enter a query using the placeholder `{entity}` to specify where the entity should be inserted.
5. **Process Data**: Click the "Process Data" button to perform the web search and extract information.
6. **View Results**: The results will be displayed in the app, and you can download them as a CSV file.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your fork.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
