# app.py
import tkinter as tk
import threading
import sounddevice as sd
import numpy as np
import queue
import time
import wave
import requests
from io import BytesIO

# Watson credentials
WATSON_STT_API_KEY = "k51lTDrEovET0LSYMFviwXq5jAJS6-XLYXT2NNWuEXI6"
WATSON_STT_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/ec83e80a-7bb7-4bd6-a5e0-cba3b79f6556"

# Settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 3  # in seconds

audio_queue = queue.Queue()
is_recording = False
stream = None

def record_callback(indata, frames, time_info, status):
    if is_recording:
        audio_queue.put(indata.copy())

def transcribe_wav_bytes(wav_bytes):
    headers = {"Content-Type": "audio/wav"}
    params = {"model": "en-IN"}
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
            return " ".join(alt["transcript"] for res in result["results"] for alt in res["alternatives"])
    else:
        print("❌ Watson STT error:", response.text)
    return None

def start_recording():
    global is_recording, stream
    is_recording = True
    status_label.config(text="🎙️ Listening", fg="green")
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16',
        callback=record_callback,
        blocksize=int(SAMPLE_RATE * CHUNK_DURATION)
    )
    stream.start()

    def process_loop():
        while is_recording:
            if not audio_queue.empty():
                chunk = audio_queue.get()

                # Convert to WAV in memory
                buffer = BytesIO()
                with wave.open(buffer, 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(2)  # int16 = 2 bytes
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(chunk.tobytes())
                buffer.seek(0)

                transcript = transcribe_wav_bytes(buffer.read())
                if transcript:
                    print("✅", transcript)
                    output_text.insert(tk.END, transcript + "\n")
                    output_text.see(tk.END)

            time.sleep(0.1)

    threading.Thread(target=process_loop, daemon=True).start()

def stop_recording():
    global is_recording, stream
    is_recording = False
    if stream:
        stream.stop()
        stream.close()
    status_label.config(text="🛑 Stopped", fg="red")
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

# GUI Setup
root = tk.Tk()
root.title("🎙️ Watson Live Transcriber")
root.geometry("500x400")

status_label = tk.Label(root, text="🔘 Ready", fg="blue")
status_label.pack(pady=5)

start_btn = tk.Button(root, text="Start", command=start_recording, bg="green", fg="white", height=2)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", command=stop_recording, bg="red", fg="white", height=2, state="disabled")
stop_btn.pack(pady=5)

output_text = tk.Text(root, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

root.mainloop()
