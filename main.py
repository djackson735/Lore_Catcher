import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_forever()
