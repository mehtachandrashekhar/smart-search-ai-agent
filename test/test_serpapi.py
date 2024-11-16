import requests
import os
from dotenv import load_dotenv

def test_serpapi(query):
    # Load API key
    load_dotenv()
    api_key = os.getenv("SERPAPI_KEY")

    # Send request to SerpAPI
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Search Results:")
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)

# Test
test_serpapi("OpenAI contact email")
