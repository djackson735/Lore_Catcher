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
        self.stop_recording_btn = QPushButton("Stop Recording")
        self.pause_recording_btn = QPushButton("Pause")
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

        button_layout.addWidget(self.start_recording_btn)
        button_layout.addWidget(self.stop_recording_btn)
        button_layout.addWidget(self.pause_recording_btn)

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
        exit_action.triggered.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.start_recording_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @asyncSlot()
    async def start_recording(self):
        await self.app.start_recording()
