import requests
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import WATSON_STT_API_KEY, WATSON_STT_URL


def list_watson_models():
    url = f"{WATSON_STT_URL}/v1/models"
    print("🔁 Fetching available Watson Speech to Text models...")

    response = requests.get(url, auth=("apikey", WATSON_STT_API_KEY))

    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"🧠 Available Speech to Text Models ({len(models)}):")
        for model in models:
            print(f"  - {model['name']} ({model['language']})")
    else:
        print("❌ Failed to fetch models.")
        print("Status:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    list_watson_models()
