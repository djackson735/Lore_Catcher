import asyncio
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from openai import OpenAI

client = OpenAI()

# Queues to ensure that the functions run concurrently
file_queue = asyncio.Queue()
clip_queue = asyncio.Queue()

# Audio recording parameters
samplerate = 44100
channels = 2
duration = 10


async def record_audio():
    chunk_number = 1
    while True:
        print(f"RECORDING chunk {chunk_number}...")
        # Record audio for 'duration' seconds
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  # Wait for the recording to finish
        # Convert the recording to a numpy array and put it in the queue
        await clip_queue.put((chunk_number, np.array(recording)))
        print(f"Chunk {chunk_number} recorded and placed in Clip Queue. Clip Queue Size: {clip_queue.qsize()}")
        chunk_number += 1
        await asyncio.sleep(0.1)


async def save_audio():
    while True:
        # Get the recording from the queue
        chunk_number, recording = await clip_queue.get()
        print(f"Saving Chunk {chunk_number}...")
        # Save the recording as a .wav file
        file_name = f'./{chunk_number}.wav'
        wavfile.write(file_name, samplerate, recording)
        print(f"Chunk {chunk_number} saved.")
        await file_queue.put(file_name)


async def whisper_api_call():
    while True:
        # Get file_name from the file_queue
        file_name = await file_queue.get()
        print(f"Sending {file_name} to Whisper API...")
        await transcribe_audio(file_name)


async def transcribe_audio(file_name):
    audio_file = open(file_name, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    print(f"Transcript: {transcript}")
    return transcript


async def main():
    # Create tasks for each function
    task1 = asyncio.create_task(record_audio())
    task2 = asyncio.create_task(save_audio())
    task3 = asyncio.create_task(whisper_api_call())

    # Wait for all tasks to complete
    await task1
    await task2
    await task3


# Run the main function
asyncio.run(main())
