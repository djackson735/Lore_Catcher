from PyQt5.QtCore import QCoreApplication

from app import Application as App
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, \
    QMenuBar, QStatusBar
from qasync import asyncSlot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = App()

        self.scroll_area = QScrollArea()
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_container)
        self.start_recording_btn = QPushButton('Start Recording', self)
        self.toggle_pause_btn = QPushButton("Pause", self)
        self.stop_recording_btn = QPushButton("Stop Recording", self)
        self.status_bar = QStatusBar()

        self.initUI()
    def initUI(self):
        self.setWindowTitle('Lore Catcher')
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        # Scroll Area
        self.scroll_area.setWidgetResizable(True)

        # Scroll Container and Layout
        self.scroll_area.setWidget(self.scroll_container)

        main_layout.addWidget(self.scroll_area)

        # Buttons
        self.start_recording_btn.clicked.connect(self.start_recording)
        self.toggle_pause_btn.clicked.connect(self.toggle_pause_resume)
        self.toggle_pause_btn.setEnabled(False)
        self.stop_recording_btn.clicked.connect(self.stop_recording)
        self.stop_recording_btn.setEnabled(False)

        button_layout.addWidget(self.start_recording_btn)
        button_layout.addWidget(self.toggle_pause_btn)
        button_layout.addWidget(self.stop_recording_btn)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

        # Status Bar
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Menu Bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close_app)

    @asyncSlot()
    async def start_recording(self):
        self.toggle_pause_btn.setEnabled(True)
        self.stop_recording_btn.setEnabled(True)
        self.start_recording_btn.setEnabled(False)
        await self.app.start_recording()

    @asyncSlot()
    async def stop_recording(self):
        self.start_recording_btn.setEnabled(True)
        self.toggle_pause_btn.setEnabled(False)
        await self.app.audio_manager.stop_recording()

    def toggle_pause_resume(self):
        self.app.audio_manager.toggle_pause_resume()
        if self.app.audio_manager.is_paused:
            self.toggle_pause_btn.setText("Resume")
        else:
            self.toggle_pause_btn.setText("Pause")

    @asyncSlot()
    async def close_app(self):
        print("close_event Triggered")
        if self.app.audio_manager.is_recording:
            await self.app.audio_manager.stop_recording()
            print("stop_recording called")
        QCoreApplication.instance().quit()
