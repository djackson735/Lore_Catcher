import asyncio
import sys
import threading

from PyQt5.QtWidgets import QApplication

from audio.audio_manager import AudioManager
from db.db_manager import DatabaseManager
from transcription.transcriber import Transcriber
from analysis.analyzer import Analyzer
from gui.main_window import MainWindow
import openai
import queue


def start_asyncio_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def run_tasks(audio_manager, transcriber, analyzer):
    save_task = asyncio.create_task(audio_manager.save_audio())
    transcribe_task = asyncio.create_task(transcriber.transcribe_audio())
    summarize_task = asyncio.create_task(analyzer.summarize_with_context())
    await asyncio.gather(save_task, transcribe_task, summarize_task)


def main():
    client = openai.Client()

    audio_chunk_queue = queue.Queue()
    file_queue = asyncio.Queue()
    transcript_queue = asyncio.Queue()

    db_manager = DatabaseManager()

    audio_manager = AudioManager(
        audio_chunk_queue=audio_chunk_queue,
        file_queue=file_queue)

    transcriber = Transcriber(
        file_queue=file_queue,
        transcript_queue=transcript_queue,
        client=client,
        db_manager=db_manager)

    analyzer = Analyzer(
        transcript_queue=transcript_queue,
        client=client,
        db_manager=db_manager)

    # main_window = MainWindow(audio_manager=audio_manager)
    # main_window.run_gui()
    app = QApplication([])
    main_window = MainWindow(audio_manager=audio_manager)
    main_window.show()
    sys.exit(app.exec_())

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_asyncio_event_loop, args=(loop,))
    t.start()

    asyncio.run_coroutine_threadsafe(run_tasks(audio_manager, transcriber, analyzer), loop)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

#
# async def main():
#     """
#     Initializes tasks for saving audio, transcribing audio,
#     and summarizing transcripts, and runs them concurrently.
#     """
#
#     client = openai.Client()
#
#     audio_chunk_queue = queue.Queue()
#     file_queue = asyncio.Queue()
#     transcript_queue = asyncio.Queue()
#
#     audio_manager = AudioManager(
#         audio_chunk_queue=audio_chunk_queue,
#         file_queue=file_queue)
#
#     transcriber = Transcriber(
#         file_queue=file_queue,
#         transcript_queue=transcript_queue,
#         client=client,
#         db_manager=db_manager)
#
#     analyzer = Analyzer(
#         transcript_queue=transcript_queue,
#         client=client,
#         db_manager=db_manager)
#
#     main_window = MainWindow(audio_manager=audio_manager)
#     main_window.run_gui()
#
#     save_task = asyncio.create_task(audio_manager.save_audio())
#     transcribe_task = asyncio.create_task(transcriber.transcribe_audio())
#     summarize_task = asyncio.create_task(analyzer.summarize_with_context())
#     await asyncio.gather(save_task, transcribe_task, summarize_task)
#
#
# if __name__ == "__main__":
#     db_manager = DatabaseManager()
#     asyncio.run(main())
