# ibm_tts_demo.py
import requests
import simpleaudio as sa
from io import BytesIO
from requests.auth import HTTPBasicAuth
from config import WATSON_TTS_API_KEY, WATSON_TTS_URL
import wave

# Replace with your credentials
API_KEY = WATSON_TTS_API_KEY
TTS_URL = WATSON_TTS_URL
VOICE = "en-US_AllisonV3Voice"  # Use only from your supported list

def synthesize_and_play(text):
    print("🔄 Synthesizing...")
    url = f"{TTS_URL}/v1/synthesize"
    headers = {"Content-Type": "application/json", "Accept": "audio/wav"}
    payload = {"text": text}

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth("apikey", API_KEY),
        params={"voice": VOICE}
    )

    if response.status_code == 200:
        print("✅ Synthesized successfully.")
        audio = BytesIO(response.content)
        with wave.open(audio, 'rb') as wav_file:
            wave_obj = sa.WaveObject.from_wave_read(wav_file)
            wave_obj.play().wait_done()
    else:
        print("❌ Watson TTS Error:", response.text)

# Test
if __name__ == "__main__":
    text_input = input("📝 Enter text to synthesize: ")
    synthesize_and_play(text_input)
