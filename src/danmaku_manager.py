from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QResizeEvent # Added for type hinting
from collections import deque
import random
from .danmaku_widget import DanmakuWidget
from .danmaku_signal import danmaku_signal
from .danmaku_model import DanmakuModel # Added for type hinting

class DanmakuManager(QWidget):
    """
    Manages the display and positioning of danmaku messages on a widget.
    It calculates available vertical positions and ensures danmakus are spaced out.
    """
    def __init__(self) -> None:
        """
        Initializes the DanmakuManager.
        Sets up attributes for translucent background and mouse tracking.
        Calculates initial available positions for danmakus.
        """
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setMouseTracking(True)

        self.available_y_queue: deque[int] = deque()
        self.min_spacing_ratio: float = 1.0 # Changed type to float for clarity
        self._calculate_available_positions()


    def _calculate_available_positions(self) -> None:
        """
        Calculates and shuffles available vertical (y) positions for danmaku display.
        The positions are based on the widget's height and minimum spacing ratio.
        """
        self.available_y_queue.clear()
        # Ensure max_available_height is an integer for range function
        max_available_height = int(self.height() // 4)
        # Ensure min_spacing is an integer for range step
        min_spacing = int(self.size().height() / 4 / 10 * self.min_spacing_ratio)
        if min_spacing <= 0: # Prevent zero or negative step in range
            min_spacing = 1 
        
        available_y_positions = []
        for y in range(0, max_available_height, min_spacing):
            available_y_positions.append(y)
        
        random.shuffle(available_y_positions)
        self.available_y_queue.extend(available_y_positions)


    def get_next_y_position(self) -> int:
        """
        Retrieves the next available y-position from the queue for a new danmaku.
        Adds a small random jitter to the position.
        If the queue is empty, defaults to 0.

        Returns:
            int: The calculated y-position for the next danmaku.
        """
        if not self.available_y_queue:
            return 0 # Default to top if no positions are available
        
        y = self.available_y_queue.popleft()
        self.available_y_queue.append(y) # Cycle the position back to the end of the queue
        
        jitter = random.randint(-5, 5)
        # Ensure position is within widget bounds
        return max(0, min(self.height() - 20, y + jitter)) # Subtract 20 to avoid danmaku going off-screen


    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Handles the resize event of the widget.
        Recalculates available y-positions when the widget size changes.

        Args:
            event (QResizeEvent): The resize event.
        """
        super().resizeEvent(event) # Call base class implementation
        self._calculate_available_positions()


    def add_danmaku(self, model: DanmakuModel) -> None:
        """
        Adds a new danmaku to the manager for display.
        Creates a DanmakuWidget with the given model and positions it.

        Args:
            model (DanmakuModel): The data model for the danmaku to be added.
        """
        screen_width = self.width()
        y = self.get_next_y_position()
        # Ensure end_pos x-coordinate makes the danmaku fully disappear
        label = DanmakuWidget(model, self, QPoint(screen_width, y), QPoint(-model.size * len(model.text), y)) 
        label.show()

