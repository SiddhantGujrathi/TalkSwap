import requests
from requests.auth import HTTPBasicAuth
import sys
import os

# Add parent directory to sys.path so config.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import WATSON_TTS_API_KEY, WATSON_TTS_URL

API_KEY = WATSON_TTS_API_KEY
TTS_URL = WATSON_TTS_URL

response = requests.get(
    f"{TTS_URL}/v1/voices",
    auth=HTTPBasicAuth('apikey', API_KEY)
)

if response.status_code == 200:
    voices = response.json()["voices"]
    for v in voices:
        print(f"{v['name']} - {v['language']} ({v['description']})")
else:
    print("Failed to fetch voices:", response.text)
