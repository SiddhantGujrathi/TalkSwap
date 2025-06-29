import requests
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import PROJECT_ID, API_KEY

def test_granite_connection():
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "version": "2023-05-29",
        "project_id": PROJECT_ID
    }

    print("🔁 Testing connection to IBM Granite API...")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ Connected to IBM Granite successfully.")
        data = response.json()
        models = [model["model_id"] for model in data.get("resources", [])]
        print(f"🧠 Available Models ({len(models)}):")
        for m in models:
            print("  -", m)
    else:
        print("❌ Failed to connect.")
        print("Status:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    test_granite_connection()
