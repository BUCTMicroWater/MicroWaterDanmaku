from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from collections import deque
import random
from .danmaku_widget import DanmakuWidget
from .danmaku_source import DanmakuSource

class DanmakuManager(QWidget):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setMouseTracking(True)

        self.available_y_queue = deque()
        self.min_spacing_ratio = 1
        self._calculate_available_positions()


    def _calculate_available_positions(self):
        """Calculates available vertical positions for danmaku."""
        self.available_y_queue.clear()
        max_available_height = self.height() // 4
        min_spacing = self.size().height() / 4 / 10 * self.min_spacing_ratio
        available_y_positions = []
        for y in range(0, max_available_height, int(min_spacing)):
            available_y_positions.append(y)
        random.shuffle(available_y_positions)
        self.available_y_queue.extend(available_y_positions)


    def get_next_y_position(self):
        """Gets the next available vertical position with random jitter."""
        if not self.available_y_queue:
            return 0
        y = self.available_y_queue.popleft()
        self.available_y_queue.append(y)
        jitter = random.randint(-5, 5)
        return max(0, min(self.height(), y + jitter))


    def resizeEvent(self, event):
        self._calculate_available_positions()


    def add_danmaku(self, model):  # Now takes a DanmakuModel
        """Adds and displays a new danmaku message."""
        screen_width = self.width()
        y = self.get_next_y_position()
        label = DanmakuWidget(model, self, QPoint(screen_width, y), QPoint(-100, y))
        label.show()
