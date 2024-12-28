import sys
import collections

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from src.danmaku_manager import DanmakuManager
from src.danmaku_source import DanmakuSource

from PyHotKey import Key, keyboard


collections.Iterable = collections.abc.Iterable 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(screen)
        self.showFullScreen()

        self.danmaku_manager = DanmakuManager()
        self.setCentralWidget(self.danmaku_manager)

        keyboard.suppress_hotkey = True
        id1 = keyboard.register_hotkey([Key.ctrl_l,Key.shift_l,"q"],None,self.close)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())