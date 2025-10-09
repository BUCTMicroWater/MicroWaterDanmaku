import sys
import collections.abc
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCloseEvent # Added for type hinting

from src.danmaku_window import DanmakuWindow
from src.danmaku_source import DanmakuSource
from src.danmaku_model import DanmakuModel
from src.danmaku_signal import danmaku_signal

from PyHotKey import Key, keyboard

collections.Iterable = collections.abc.Iterable

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """
        Initializes the main window of the Danmaku Control Panel.
        Sets up the UI elements, layout, styles, and connects signals.
        """
        super().__init__()
        self.setWindowTitle("弹幕控制面板")
        self.resize(450, 450)
        
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
            QListWidget {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: #ffffff;
                padding: 5px;
            }
        """)

        screen_count = QApplication.desktop().screenCount()
        self.danmaku_windows: list[DanmakuWindow] = []
        for i in range(screen_count):
            danmaku_window = DanmakuWindow(i)
            self.danmaku_windows.append(danmaku_window)
        
        self.danmaku_windows_visible: bool = True
        self.danmaku_list_items: dict[str, QListWidgetItem] = {}  # Stores mapping from danmaku ID to list item

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
        text_label = QLabel("弹幕内容：")
        self.text_input = QLineEdit() # Made instance variable for potential future access
        self.text_input.setPlaceholderText("输入弹幕文本")
        text_layout.addWidget(text_label, 1)
        text_layout.addWidget(self.text_input, 4)
        input_group.addLayout(text_layout)
        
        batch_layout = QHBoxLayout()
        batch_label = QLabel("弹幕数量：")
        self.batch_input = QLineEdit() # Made instance variable
        self.batch_input.setPlaceholderText("输入弹幕条数")
        self.batch_input.setToolTip("输入弹幕条数，默认为1")
        self.batch_input.setText("1")
        batch_layout.addWidget(batch_label, 1)
        batch_layout.addWidget(self.batch_input, 4)
        input_group.addLayout(batch_layout)
        
        main_layout.addLayout(input_group)
        
        send_button = QPushButton("发送弹幕")
        send_button.clicked.connect(lambda: self.send_batch_danmaku(self.text_input.text(), self.batch_input.text()))
        send_button.setShortcut("Ctrl+Enter")
        send_button.setStyleSheet("background-color: #2196F3;")
        main_layout.addWidget(send_button)
        
        # Add danmaku list label
        danmaku_list_label = QLabel("弹幕列表：")
        main_layout.addWidget(danmaku_list_label)
        
        # Add danmaku list widget
        self.danmaku_list = QListWidget()
        self.danmaku_list.setMinimumHeight(100)
        self.danmaku_list.setSelectionMode(QListWidget.SingleSelection)
        main_layout.addWidget(self.danmaku_list)
        
        # Add recall button
        recall_button = QPushButton("撤回选中弹幕")
        recall_button.clicked.connect(self.recall_selected_danmaku)
        recall_button.setStyleSheet("background-color: #FF9800;")
        main_layout.addWidget(recall_button)
        
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
        
        shortcut_label = QLabel("快捷键：Ctrl+Enter 发送 | Ctrl+Shift+Q 退出")
        shortcut_label.setStyleSheet("color: #777; font-size: 12px;")
        shortcut_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(shortcut_label)
        
        self.setCentralWidget(main_widget)
        
        self.danmaku_source = DanmakuSource()
        self.danmaku_source.start()

        keyboard.suppress_hotkey = True
        keyboard.register_hotkey([Key.ctrl_l,Key.shift_l,"q"],None,self.close_all)

        # Connect signals for adding and removing danmaku
        danmaku_signal.danmaku_signal_add.connect(self.add_danmaku_and_update_list)
        danmaku_signal.danmaku_signal_delete.connect(self.remove_danmaku_from_list)

    def close_all(self) -> None:
        """
        Closes the main application window.
        This method is typically connected to an exit button or shortcut.
        """
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handles the window close event.
        Ensures all danmaku windows are closed and the danmaku source thread is properly terminated.

        Args:
            event (QCloseEvent): The close event.
        """
        for danmaku_window in self.danmaku_windows:
            danmaku_window.close()
        
        if hasattr(self, 'danmaku_source') and self.danmaku_source.isRunning():
            self.danmaku_source.quit()
            if not self.danmaku_source.wait(3000): # Wait for 3 seconds
                self.danmaku_source.terminate() # Force terminate if not quit
                self.danmaku_source.wait() # Wait for termination
        
        event.accept()

    def toggle_danmaku_windows(self) -> None:
        """
        Toggles the visibility of all danmaku windows.
        If visible, they become hidden, and vice-versa.
        """
        self.danmaku_windows_visible = not self.danmaku_windows_visible
        for danmaku_window in self.danmaku_windows:
            if self.danmaku_windows_visible:
                danmaku_window.show()
            else:
                danmaku_window.hide()
                                 
    def add_danmaku_and_update_list(self, model: DanmakuModel) -> None:
        """
        Adds a danmaku to all visible danmaku windows and updates the central list widget.

        Args:
            model (DanmakuModel): The danmaku data model to add.
        """
        # Add to danmaku windows first
        for danmaku_window in self.danmaku_windows:
            if danmaku_window.isVisible():
                 danmaku_window.add_danmaku(model)
        
        # Add danmaku to the list
        item_text = f"{model.danmaku_id}: {model.text}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, model.danmaku_id)  # Store danmaku ID as user data
        self.danmaku_list.addItem(item)
        self.danmaku_list.scrollToBottom()  # Scroll to the bottom
        
        # Store the mapping between danmaku ID and list item
        self.danmaku_list_items[model.danmaku_id] = item
                 
    def remove_danmaku_from_list(self, danmaku_id: str) -> None:
        """
        Removes a danmaku from the central list widget based on its ID.

        Args:
            danmaku_id (str): The ID of the danmaku to remove.
        """
        # Remove from the list
        if danmaku_id in self.danmaku_list_items:
            item = self.danmaku_list_items[danmaku_id]
            row = self.danmaku_list.row(item)
            self.danmaku_list.takeItem(row)
            del self.danmaku_list_items[danmaku_id]
    
    def recall_selected_danmaku(self) -> None:
        """
        Recalls (removes) the currently selected danmaku from the list.
        This emits a signal to trigger the removal process.
        """
        selected_items = self.danmaku_list.selectedItems()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        danmaku_id = selected_item.data(Qt.UserRole)
        if danmaku_id:
            # Emit signal to remove danmaku
            danmaku_signal.danmaku_signal_delete.emit(danmaku_id)

    def send_batch_danmaku(self, text: str, batch_str: str, color: str = "#FFFFFF", size: int = 20) -> None:
        """
        Sends a batch of danmakus.
        The number of danmakus is determined by batch_str.
        Each danmaku is scheduled with a random delay.

        Args:
            text (str): The text content of the danmaku.
            batch_str (str): A string representing the number of danmakus to send. Defaults to 1 if invalid.
            color (str, optional): The color of the danmaku text. Defaults to "#FFFFFF".
            size (int, optional): The font size of the danmaku. Defaults to 20.
        """
        try:
            batch_count = int(batch_str)
            if batch_count <= 0:
                batch_count = 1
        except ValueError:
            batch_count = 1
        
        self._schedule_next_danmaku(text, color, size, batch_count)

    def _schedule_next_danmaku(self, text: str, color: str, size: int, remaining_count: int) -> None:
        """
        Schedules the sending of the next danmaku in a batch.
        If remaining_count > 0, it creates a DanmakuModel, emits a signal to add it,
        and then schedules the next one with a random delay.

        Args:
            text (str): The text content of the danmaku.
            color (str): The color of the danmaku text.
            size (int): The font size of the danmaku.
            remaining_count (int): The number of danmakus remaining to be sent in the current batch.
        """
        if remaining_count <= 0:
            return

        current_model = DanmakuModel(text=text, color=color, size=size)
        # Send danmaku using signal
        danmaku_signal.danmaku_signal_add.emit(current_model)

        new_remaining_count = remaining_count - 1
        if new_remaining_count > 0:
            delay_ms = int(random.uniform(500, 3000)) # Random delay between 0.5 and 3 seconds
            QTimer.singleShot(delay_ms, lambda: self._schedule_next_danmaku(text, color, size, new_remaining_count))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())