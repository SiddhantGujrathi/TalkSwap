# granite/granite_client.py

import base64
import requests
from config import API_KEY, PROJECT_ID, GRANITE_MODEL_ID, API_URL

def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("❌ Failed to get access token:", response.text)
        return None

def generate_text_from_prompt(prompt):
    access_token = get_access_token()
    if not access_token:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": GRANITE_MODEL_ID,
        "input": prompt,
        "project_id": PROJECT_ID,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 100
        }
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['results'][0]['generated_text']
    else:
        print("❌ Granite error:", response.text)
        return None
    

def detect_language_from_text(text):
    prompt = f"Detect the language of this sentence: \"{text}\". Respond only with the language code like en, hi, fr, etc."
    response = generate_text_from_prompt(prompt)
    if response:
        return response.strip().split()[0].lower()
    return "en"
   
def translate_text_with_granite(text, src_lang_code, target_lang_code):
    prompt = (
        f"Translate the following sentence from {src_lang_code.upper()} to {target_lang_code.upper()}.\n"
        f"⚠️ Respond with the translated sentence only in {target_lang_code.upper()}. "
        f"No explanation. Do not add any title and Do not show the original sentence. No language name or code. No formatting.\n\n"
        f"{text}"
    )
    return generate_text_from_prompt(prompt).strip()



