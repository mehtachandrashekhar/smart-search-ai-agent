import requests
import os
from dotenv import load_dotenv

def test_openai(prompt):
    # Load API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # OpenAI API endpoint
    url = "https://api.openai.com/v1/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 100,
    }

    # Send request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("OpenAI Response:")
        print(response.json()["choices"][0]["text"].strip())
    else:
        print("Error:", response.status_code, response.text)

# Test
test_openai("Extract the email address from: 'Contact us at info@openai.com'")
