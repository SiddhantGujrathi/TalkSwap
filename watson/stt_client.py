# watson/stt_client.py
import requests
from config import WATSON_STT_API_KEY, WATSON_STT_URL

def transcribe_with_watson(wav_bytes, language="en-IN"):
    headers = {"Content-Type": "audio/wav"}
    params = {"model": language}
    response = requests.post(
        f"{WATSON_STT_URL}/v1/recognize",
        headers=headers,
        params=params,
        auth=("apikey", WATSON_STT_API_KEY),
        data=wav_bytes
    )
    if response.status_code == 200:
        result = response.json()
        if result.get("results"):
            return " ".join(
                alt["transcript"] for res in result["results"] for alt in res["alternatives"]
            )
    else:
        print("❌ Watson STT error:", response.text)
    return None
