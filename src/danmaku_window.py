from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from src.danmaku_manager import DanmakuManager

class DanmakuWindow(QMainWindow):
    def __init__(self, index):
        super().__init__()

        if index < 0:
            raise ValueError("index must be a non-negative integer")
        
        self.index = index

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Get the available screens
        screens = QGuiApplication.screens()
        if index >= len(screens):
            raise ValueError(f"Invalid screen index {index}. Maximum index is {len(screens) - 1}")
            
        screen_geometry = screens[index].geometry()
        
        # Set window geometry and show on correct screen
        print(f"Setting geometry for screen {index}: {screen_geometry}")
        self.show()
        
        # Move to the correct screen explicitly
        self.windowHandle().setScreen(screens[index])
        self.setGeometry(screen_geometry)
        # Force the window to be positioned correctly
        self.move(screen_geometry.x(), screen_geometry.y())

        self.danmaku_manager = DanmakuManager()
        self.setCentralWidget(self.danmaku_manager)

    def add_danmaku(self, model):
        print("Index ",self.index," add_danmaku called")
        self.danmaku_manager.add_danmaku(model)