# app.py
import tkinter as tk
import threading
import sounddevice as sd
import queue
import time
import numpy as np

from audio.chunk_buffer import AudioChunkBuffer
from utils.audio_utils import numpy_to_wav_bytes
from watson.stt_client import transcribe_with_watson
from granite.granite_client import translate_text_with_granite

# Constants
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 2  # seconds

audio_queue = queue.Queue()
buffer = AudioChunkBuffer(max_chunks=3)
is_recording = False
stream = None

# Language options
LANGUAGE_OPTIONS = {
    "English (India)": "en-IN",
    "Hindi": "hi-IN_BroadbandModel",
    "English (US)": "en-US_BroadbandModel",
    "Marathi": "mr-IN_BroadbandModel",
    "French": "fr-FR_BroadbandModel",
    "German": "de-DE_BroadbandModel",
    "Spanish": "es-ES_BroadbandModel",
    "Japanese": "ja-JP_BroadbandModel",
    "Chinese (Mandarin)": "zh-CN_BroadbandModel",
    "Arabic": "ar-MS_BroadbandModel",
    "Korean": "ko-KR_BroadbandModel"
}

TRANSLATION_LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Korean": "ko"
}

selected_lang = None
selected_target_lang = None

def record_callback(indata, frames, time_info, status):
    if is_recording:
        audio_queue.put(indata.copy())

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
            try:
                chunk = audio_queue.get(timeout=0.2)
                buffer.add_chunk(chunk)

                combined = buffer.get_combined()
                wav_bytes = numpy_to_wav_bytes(combined, SAMPLE_RATE)

                model = LANGUAGE_OPTIONS[selected_lang.get()]
                transcript = transcribe_with_watson(wav_bytes, model)

                if transcript:
                    print("📝 Transcription:", transcript)
                    output_text.insert(tk.END, transcript + "\n")
                    output_text.see(tk.END)

                    # Translate
                    src_lang_code = TRANSLATION_LANG_CODES[selected_lang.get().split()[0]]
                    target_lang_code = TRANSLATION_LANG_CODES[selected_target_lang.get()]
                    translated = translate_text_with_granite(transcript, src_lang_code, target_lang_code)

                    if translated:
                        translated_text.insert(tk.END, translated + "\n")
                        translated_text.see(tk.END)
                        print("🌐 Translation:", translated)

                buffer.clear()

            except queue.Empty:
                continue

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
root.title("🎙️ Watson + Granite Translator")
root.geometry("500x600")

status_label = tk.Label(root, text="🔘 Ready", fg="blue")
status_label.pack(pady=5)

# 🔽 Source Language
lang_frame = tk.Frame(root)
lang_frame.pack(pady=5)
tk.Label(lang_frame, text="🎤 Source Language:").pack(side=tk.LEFT, padx=(0, 10))
selected_lang = tk.StringVar(value="English (India)")
tk.OptionMenu(lang_frame, selected_lang, *LANGUAGE_OPTIONS.keys()).pack(side=tk.LEFT)

# 🔽 Target Translation Language
target_frame = tk.Frame(root)
target_frame.pack(pady=5)
tk.Label(target_frame, text="🌐 Translate To:").pack(side=tk.LEFT, padx=(0, 10))
selected_target_lang = tk.StringVar(value="Hindi")
tk.OptionMenu(target_frame, selected_target_lang, *TRANSLATION_LANG_CODES.keys()).pack(side=tk.LEFT)

# 🔘 Controls
start_btn = tk.Button(root, text="Start", command=start_recording, bg="green", fg="white", height=2)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", command=stop_recording, bg="red", fg="white", height=2, state="disabled")
stop_btn.pack(pady=5)

# 📄 Transcription Output
tk.Label(root, text="📝 Transcription Output").pack()
output_text = tk.Text(root, wrap=tk.WORD, height=8)
output_text.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

# 🌍 Translation Output
tk.Label(root, text="🌐 Translated Output").pack()
translated_text = tk.Text(root, wrap=tk.WORD, height=8, bg="#eef6ff")
translated_text.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

root.mainloop()
