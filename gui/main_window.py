from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QScrollArea, QStatusBar, QMenuBar, QFrame
import sys


class MainWindow(QMainWindow):
    def __init__(self, audio_manager, *args, **kwargs):
        super().__init__()
        self.audio_manager = audio_manager

        self.setWindowTitle("Lore Catcher")
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
        self.start_recording_btn = QPushButton("Start Recording")
        self.stop_recording_btn = QPushButton("Stop Recording")
        self.pause_recording_btn = QPushButton("Pause")

        button_layout.addWidget(self.start_recording_btn)
        button_layout.addWidget(self.stop_recording_btn)
        button_layout.addWidget(self.pause_recording_btn)

        # Buttons to Layout
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

        # Connect buttons to methods
        self.start_recording_btn.clicked.connect(self.audio_manager.start_recording_thread)
        # self.stop_recording_btn.clicked.connect(self.stop_recording_btn)
        # self.pause_recording_btn.clicked.connect(self.pause_recording_btn)

    def append_summary(self, summary):
        # Create a new label for the summary
        summary_label = QLabel(summary)
        summary_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        summary_label.setWordWrap(True)

        # Add the label to the scroll layout
        self.scroll_layout.addWidget(summary_label)

        # Auto-scroll to the bottom
        self.auto_scroll()

    def auto_scroll(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    # def run_gui(self):
    #     print("Running GUI")
    #     app = QApplication(sys.argv)
    #
    #     window = MainWindow(self.audio_manager)
    #     window.show()
    #     sys.exit(app.exec_())
