# watson/tts_client.py
import requests
from config import WATSON_TTS_API_KEY, WATSON_TTS_URL

def synthesize_speech(text, voice="hi-IN_AnanyaV3Voice"):
    headers = {
        "Content-Type": "application/json",
    }
    auth = ("apikey", WATSON_TTS_API_KEY)
    params = {
        "accept": "audio/wav",
        "voice": voice
    }
    payload = {
        "text": text
    }

    response = requests.post(
        f"{WATSON_TTS_URL}/v1/synthesize",
        headers=headers,
        params=params,
        json=payload,
        auth=auth
    )

    if response.status_code == 200:
        return response.content  # WAV bytes
    else:
        print("❌ Watson TTS error:", response.text)
        return None
