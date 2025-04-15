import sys
import collections

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from src.danmaku_window import DanmakuWindow
from src.danmaku_source import DanmakuSource

from PyHotKey import Key, keyboard


collections.Iterable = collections.abc.Iterable 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen_count = QApplication.desktop().screenCount()
        self.danmaku_windows = []
        for i in range(screen_count):
            danmaku_window = DanmakuWindow(i)
            self.danmaku_windows.append(danmaku_window)

        self.danmaku_source = DanmakuSource()
        self.danmaku_source.danmakuSignal.connect(self.add_danmaku)
        self.danmaku_source.start()

        keyboard.suppress_hotkey = True
        keyboard.register_hotkey([Key.ctrl_l,Key.shift_l,"q"],None,self.close_all)

    def close_all(self):
        for danmaku_window in self.danmaku_windows:
            danmaku_window.close()
        self.close()
    
    def add_danmaku(self, model):
        for danmaku_window in self.danmaku_windows:
            danmaku_window.add_danmaku(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())