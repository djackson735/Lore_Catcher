import asyncio
import queue
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from openai import OpenAI
import datetime
import threading

client = OpenAI()

# Thread safe queue for record_audio
audio_chunk_queue = queue.Queue()

# Asyncio queues for processing tasks
file_queue = asyncio.Queue()
transcript_queue = asyncio.Queue()

# Audio recording parameters
samplerate = 44100
channels = 2
duration = 20


def record_audio():
    """
    Continuously records audio in chunks and places them in the audio_chunk_queue.

    This function runs in a separate thread to ensure continuous recording
    without interruption.

    The recorded audio chunks are saved as numpy arrays.
    """
    chunk_number = 1
    stream = sd.InputStream(samplerate=samplerate, channels=channels)
    stream.start()

    while True:
        print(f"{datetime.datetime.now()} - RECORDING started")
        print(f"RECORDING chunk {chunk_number}...")
        recording, _ = stream.read(int(duration * samplerate))

        audio_chunk_queue.put((chunk_number, np.array(recording)))
        chunk_number += 1


async def save_audio():
    """
    Saves audio chunks from the audio_chunk_queue to .wav files.

    The saved file paths are placed into the file_queue for further processing.
    """
    while True:
        chunk_number, recording = await asyncio.to_thread(audio_chunk_queue.get)
        print(f"{datetime.datetime.now()} - Saving audio started on chunk {chunk_number}")
        file_path = f'./{chunk_number}.wav'

        try:
            wavfile.write(file_path, samplerate, recording)
            print(f"Chunk {chunk_number} saved.")
        except Exception as e:
            print(f"Error saving chunk {chunk_number}: {e}")
            continue

        await file_queue.put(file_path)


async def transcribe_audio():
    """
    Transcribes audio files from the file_queue using OpenAI's Whisper API.

    The transcriptions are placed into the transcript_queue.
    """
    while True:
        file_name = await file_queue.get()
        print(f"{datetime.datetime.now()} - Transcribing audio started on file {file_name}")

        try:
            audio_file = open(file_name, "rb")
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            print(f"Transcript: {transcript}")
            await transcript_queue.put(transcript)

        except Exception as e:
            print(f"Error transcribing file {file_name}: {e}")

        finally:
            file_queue.task_done()


async def summarize_transcript():
    """
    Summarizes transcripts from the transcript_queue using OpenAI's GPT-3.5-turbo model.
    """
    while True:
        transcript = await transcript_queue.get()
        print(f"{datetime.datetime.now()} - Summarizing transcript started")

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Your task is to summarize a section of a transcript that is being passed to you. The " +
                            "challenge is that the section you're given is part of a larger transcript, and may " +
                            "start or end in the middle of a sentence. Summarize it succinctly, using context clues " +
                            "to understand the beginning and where it's going."
                        )
                    },
                    {
                        "role": "user",
                        "content": transcript
                    }
                ]
            )
            summary = completion.choices[0].message.content
            print(f"Summary: {summary}")
        except Exception as e:
            print(f"Error summarizing transcript: {e}")

        transcript_queue.task_done()


async def main():
    """
    Initializes tasks for saving audio, transcribing audio,
    and summarizing transcripts, and runs them concurrently.
    """
    save_task = asyncio.create_task(save_audio())
    transcribe_task = asyncio.create_task(transcribe_audio())
    summarize_task = asyncio.create_task(summarize_transcript())

    await asyncio.gather(save_task, transcribe_task, summarize_task)


if __name__ == "__main__":
    # Start the recording thread
    recording_thread = threading.Thread(target=record_audio, daemon=True)
    recording_thread.start()

    # Run the asyncio event loop for other tasks
    asyncio.run(main())
