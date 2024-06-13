import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import datetime
import asyncio


class AudioManager:
    """
        AudioManager is a class for managing audio recording and saving.

        Attributes:
            samplerate (int): The sample rate for the audio recording.
            channels (int): The number of audio channels.
            duration (int): The duration of the audio recording in seconds.
            audio_chunk_queue (queue): A queue for storing audio chunks.
            file_queue (queue): A queue for storing file paths of saved audio chunks.
            is_recording (bool): A flag indicating whether recording is in progress.
            is_paused (bool): A flag indicating whether recording is paused.

        Note: OpenAI's Whisper API has a 25 mb limit on audio file size.
        """

    def __init__(
            self,
            samplerate=32000,
            channels=2,
            duration=15,
            audio_chunk_queue=None,
            file_queue=None):

        self.samplerate = samplerate
        self.channels = channels
        self.duration = duration
        self.audio_chunk_queue = audio_chunk_queue
        self.file_queue = file_queue
        self.is_recording = False
        self.is_paused = False
        self.recording_thread = None

    def start_recording_thread(self):
        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()

    def record_audio(self):
        """
        Records audio in one second segments until duration is reached, then adds the chunk to the audio_chunk_queue.
        """
        chunk_number = 1
        segment_number = 1
        accumulated_segments = []
        segment_duration = 1
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels) as stream:

            while self.is_recording:
                if self.is_paused:
                    sd.sleep(1)
                    continue

                print(f"{datetime.datetime.now()} - RECORDING started")
                print(f"RECORDING segment {segment_number}...")

                # Record a one-second segment
                segment, _ = stream.read(int(segment_duration * self.samplerate))
                accumulated_segments.append(segment)
                segment_number += 1

                # Determine if the duration has been reached
                if len(accumulated_segments) >= self.duration:
                    # Flatten the accumulated segments and add to the audio_chunk_queue
                    self.audio_chunk_queue.put((chunk_number, np.concatenate(accumulated_segments)))
                    accumulated_segments = []
                    print(f"Chunk {chunk_number} added to queue.")
                    chunk_number += 1

    def toggle_pause_resume(self):
        self.is_paused = not self.is_paused

    async def stop_recording(self):
        self.is_paused = False
        self.is_recording = False

        if self.is_recording is not None:
            print(f"{datetime.datetime.now()} - Stopping recording...")
            self.recording_thread.join()
            self.recording_thread = None
            print(f"{datetime.datetime.now()} - Recording stopped.")

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
