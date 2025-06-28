# audio/chunk_buffer.py
import numpy as np

class AudioChunkBuffer:
    def __init__(self, max_chunks=3):
        self.buffer = []
        self.max_chunks = max_chunks

    def add_chunk(self, chunk):
        self.buffer.append(chunk)
        if len(self.buffer) > self.max_chunks:
            self.buffer.pop(0)

    def get_combined(self):
        return np.concatenate(self.buffer, axis=0)

    def clear(self):
        self.buffer.clear()
