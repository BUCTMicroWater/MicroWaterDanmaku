import sys
import collections
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout ,QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer

from src.danmaku_window import DanmakuWindow
from src.danmaku_source import DanmakuSource
from src.danmaku_model import DanmakuModel

from PyHotKey import Key, keyboard


collections.Iterable = collections.abc.Iterable 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("弹幕控制面板")
        self.resize(450, 250)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #398438;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                font-weight: bold;
            }
        """)

        screen_count = QApplication.desktop().screenCount()
        self.danmaku_windows = []
        for i in range(screen_count):
            danmaku_window = DanmakuWindow(i)
            self.danmaku_windows.append(danmaku_window)
        
        self.danmaku_windows_visible = True

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title_label = QLabel("弹幕发送控制")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        input_group = QVBoxLayout()
        
        text_layout = QHBoxLayout()
        text_label = QLabel("弹幕内容:")
        text_input = QLineEdit()
        text_input.setPlaceholderText("输入弹幕文本")
        text_layout.addWidget(text_label, 1)
        text_layout.addWidget(text_input, 4)
        input_group.addLayout(text_layout)
        
        batch_layout = QHBoxLayout()
        batch_label = QLabel("弹幕数量:")
        batch_input = QLineEdit()
        batch_input.setPlaceholderText("输入弹幕条数")
        batch_input.setToolTip("输入弹幕条数，默认为1")
        batch_input.setText("1")
        batch_layout.addWidget(batch_label, 1)
        batch_layout.addWidget(batch_input, 4)
        input_group.addLayout(batch_layout)
        
        main_layout.addLayout(input_group)
        
        send_button = QPushButton("发送弹幕")
        send_button.clicked.connect(lambda: self.send_batch_danmaku(text_input.text(), batch_input.text()))
        send_button.setShortcut("Ctrl+Enter")
        send_button.setStyleSheet("background-color: #2196F3;")
        main_layout.addWidget(send_button)
        
        buttons_layout = QHBoxLayout()
        hide_button = QPushButton("隐藏/显示弹幕")
        hide_button.clicked.connect(self.toggle_danmaku_windows)
        exit_button = QPushButton("退出")
        exit_button.setStyleSheet("background-color: #f44336;")
        exit_button.clicked.connect(self.close_all)
        exit_button.setShortcut("Ctrl+Q")
        
        buttons_layout.addWidget(hide_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(exit_button)
        main_layout.addLayout(buttons_layout)
        
        shortcut_label = QLabel("快捷键: Ctrl+Enter 发送 | Ctrl+Shift+Q 退出")
        shortcut_label.setStyleSheet("color: #777; font-size: 12px;")
        shortcut_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(shortcut_label)
        
        self.setCentralWidget(main_widget)
        
        self.danmaku_source = DanmakuSource()
        self.danmaku_source.danmakuSignal.connect(self.add_danmaku)
        self.danmaku_source.start()

        keyboard.suppress_hotkey = True
        keyboard.register_hotkey([Key.ctrl_l,Key.shift_l,"q"],None,self.close_all)

    def close_all(self):
        self.close()

    def closeEvent(self, event):
        for danmaku_window in self.danmaku_windows:
            danmaku_window.close()
        
        if hasattr(self, 'danmaku_source') and self.danmaku_source.isRunning():
            self.danmaku_source.quit()
            if not self.danmaku_source.wait(3000):
                self.danmaku_source.terminate()
                self.danmaku_source.wait()
        
        event.accept()

    def toggle_danmaku_windows(self):
        self.danmaku_windows_visible = not self.danmaku_windows_visible
        for danmaku_window in self.danmaku_windows:
            if self.danmaku_windows_visible:
                danmaku_window.show()
            else:
                danmaku_window.hide()
    
    def add_danmaku(self, model):
        for danmaku_window in self.danmaku_windows:
            if danmaku_window.isVisible():
                 danmaku_window.add_danmaku(model)

    def send_batch_danmaku(self, text, batch_str, color="#FFFFFF", size=20):
        try:
            batch_count = int(batch_str)
            if batch_count <= 0:
                batch_count = 1
        except ValueError:
            batch_count = 1
        
        self._schedule_next_danmaku(text, color, size, batch_count)

    def _schedule_next_danmaku(self, text, color, size, remaining_count):
        if remaining_count <= 0:
            return

        current_model = DanmakuModel(text=text, color=color, size=size)
        self.add_danmaku(current_model)

        new_remaining_count = remaining_count - 1
        if new_remaining_count > 0:
            delay_ms = int(random.uniform(500, 3000))
            QTimer.singleShot(delay_ms, lambda: self._schedule_next_danmaku(text, color, size, new_remaining_count))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())