# utils/audio_utils.py
import wave
from io import BytesIO

def numpy_to_wav_bytes(data, sample_rate):
    buffer = BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit = 2 bytes
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())
    buffer.seek(0)
    return buffer.read()
