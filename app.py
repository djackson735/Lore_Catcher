import openai
import queue
import asyncio
from audio.audio_manager import AudioManager
from db.db_manager import DatabaseManager
from transcription.transcriber import Transcriber
from analysis.analyzer import Analyzer


class Application:
    def __init__(self):
        self.client = openai.Client()
        self.audio_chunk_queue = queue.Queue()
        self.file_queue = asyncio.Queue()
        self.transcript_queue = asyncio.Queue()
        self.db_manager = DatabaseManager()

        self.audio_manager = AudioManager(
            audio_chunk_queue=self.audio_chunk_queue,
            file_queue=self.file_queue)

        self.transcriber = Transcriber(
            file_queue=self.file_queue,
            transcript_queue=self.transcript_queue,
            client=self.client,
            db_manager=self.db_manager)

        self.analyzer = Analyzer(
            transcript_queue=self.transcript_queue,
            client=self.client,
            db_manager=self.db_manager)

    async def start_recording(self):
        self.audio_manager.is_recording = True
        self.audio_manager.start_recording_thread()
        save_task = asyncio.create_task(self.audio_manager.save_audio())
        transcribe_task = asyncio.create_task(self.transcriber.transcribe_audio())
        summarize_task = asyncio.create_task(self.analyzer.summarize_with_context())
        await asyncio.gather(save_task, transcribe_task, summarize_task)
