import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import datetime
import asyncio


class AudioManager:
    def __init__(
            self,
            samplerate=32000,
            channels=2,
            duration=20,
            audio_chunk_queue=None,
            file_queue=None):

        self.samplerate = samplerate
        self.channels = channels
        self.duration = duration
        self.audio_chunk_queue = audio_chunk_queue
        self.file_queue = file_queue

    # TODO: Investigate whether or not you need a stop event for the recording thread.
    def record_audio(self):
        """
        Continuously records audio in chunks and places them in the audio_chunk_queue.
        """
        chunk_number = 1
        stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels)
        stream.start()

        while True:
            print(f"{datetime.datetime.now()} - RECORDING started")
            print(f"RECORDING chunk {chunk_number}...")
            recording, _ = stream.read(int(self.duration * self.samplerate))
            self.audio_chunk_queue.put((chunk_number, np.array(recording)))
            chunk_number += 1

    def start_recording_thread(self):
        recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        recording_thread.start()

    async def save_audio(self):
        """
        Saves audio chunks from the audio_chunk_queue to .wav files.
        """
        while True:
            chunk_number, recording = await asyncio.to_thread(self.audio_chunk_queue.get)
            print(f"{datetime.datetime.now()} - Saving audio started on chunk {chunk_number}")
            file_path = f'./{chunk_number}.wav'

            try:
                wavfile.write(file_path, self.samplerate, recording)
                print(f"Chunk {chunk_number} saved.")
            except Exception as e:
                print(f"Error saving chunk {chunk_number}: {e}")
                continue

            await self.file_queue.put(file_path)
