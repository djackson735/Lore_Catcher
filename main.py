import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, \
    QMenuBar, QStatusBar
from audio.audio_manager import AudioManager
from db.db_manager import DatabaseManager
from transcription.transcriber import Transcriber
from analysis.analyzer import Analyzer
import openai
import queue
from qasync import QEventLoop, asyncSlot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio_chunk_queue = queue.Queue()
        self.file_queue = asyncio.Queue()
        self.transcript_queue = asyncio.Queue()
        self.client = openai.Client()
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

    def initUI(self):
        self.setWindowTitle('Lore Catcher')
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        # Summaries Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Scroll Container and Layout
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_container)
        self.scroll_area.setWidget(self.scroll_container)

        main_layout.addWidget(self.scroll_area)

        # Buttons
        self.start_recording_btn = QPushButton('Start Recording', self)
        self.start_recording_btn.clicked.connect(self.start_recording)
        button_layout.addWidget(self.start_recording_btn)

        self.stop_recording_btn = QPushButton("Stop Recording")
        button_layout.addWidget(self.stop_recording_btn)

        self.pause_recording_btn = QPushButton("Pause")
        button_layout.addWidget(self.pause_recording_btn)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Menu Bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.start_recording_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @asyncSlot()
    async def start_recording(self):
        self.audio_manager.start_recording_thread()

        save_task = asyncio.create_task(self.audio_manager.save_audio())
        transcribe_task = asyncio.create_task(self.transcriber.transcribe_audio())
        summarize_task = asyncio.create_task(self.analyzer.summarize_with_context())
        await asyncio.gather(save_task, transcribe_task, summarize_task)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_forever()
