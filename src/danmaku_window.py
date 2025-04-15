from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from src.danmaku_manager import DanmakuManager

class DanmakuWindow(QMainWindow):
    def __init__(self, index):
        if index < 0:
            raise ValueError("index must be a non-negative integer")
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QApplication.desktop().screenGeometry(index)
        self.setGeometry(screen)
        self.showFullScreen()

        self.danmaku_manager = DanmakuManager()
        self.setCentralWidget(self.danmaku_manager)