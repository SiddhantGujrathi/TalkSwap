import requests
from requests.auth import HTTPBasicAuth
from config import WATSON_TTS_API_KEY, WATSON_TTS_URL

# Replace with your own credentials
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
