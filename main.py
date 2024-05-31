import asyncio
from audio.audio_manager import AudioManager
from db.db_manager import DatabaseManager
from transcription.transcriber import Transcriber
from analysis.analyzer import Analyzer
import openai
import queue


async def main():
    """
    Initializes tasks for saving audio, transcribing audio,
    and summarizing transcripts, and runs them concurrently.
    """

    client = openai.Client()

    audio_chunk_queue = queue.Queue()
    file_queue = asyncio.Queue()
    transcript_queue = asyncio.Queue()

    audio_manager = AudioManager(
        audio_chunk_queue=audio_chunk_queue,
        file_queue=file_queue)

    transcriber = Transcriber(
        file_queue=file_queue,
        transcript_queue=transcript_queue,
        client=client)

    analyzer = Analyzer(
        transcript_queue=transcript_queue,
        client=client,
        db_manager=db_manager)

    audio_manager.start_recording_thread()

    save_task = asyncio.create_task(audio_manager.save_audio())
    transcribe_task = asyncio.create_task(transcriber.transcribe_audio())
    summarize_task = asyncio.create_task(analyzer.summarize_transcript())

    await asyncio.gather(save_task, transcribe_task, summarize_task)


if __name__ == "__main__":
    db_manager = DatabaseManager()
    asyncio.run(main())
