from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QRect  # Added QRect for type hinting
from PyQt5.QtGui import QGuiApplication, QScreen  # Added QScreen for type hinting

from .danmaku_manager import DanmakuManager
from .danmaku_model import DanmakuModel  # Added for type hinting


class DanmakuWindow(QMainWindow):
    """
    A QMainWindow that serves as a transparent overlay for displaying danmakus on a specific screen.
    It is frameless, stays on top, and allows mouse events to pass through.
    """

    def __init__(self, screen_index: int) -> None:  # Changed: index to screen_index for clarity
        """
        Initializes the DanmakuWindow on the specified screen.

        Args:
            screen_index (int): The index of the screen on which this window will be displayed.

        Raises:
            ValueError: If screen_index is negative or invalid.
        """
        super().__init__()

        if screen_index < 0:
            raise ValueError("Screen index must be a non-negative integer.")

        self.screen_index: int = screen_index

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Get the available screens
        screens: list[QScreen] = QGuiApplication.screens()
        if not screens:
            raise RuntimeError("No screens available.")  # Handle case with no screens
        if screen_index >= len(screens):
            raise ValueError(
                f"Invalid screen index {screen_index}. Maximum index is {len(screens) - 1}."
            )

        target_screen: QScreen = screens[screen_index]
        screen_geometry: QRect = target_screen.geometry()

        # Set window geometry and show on correct screen
        # It's important to show the window before trying to move it to a specific screen
        self.show()

        # Move to the correct screen explicitly
        if self.windowHandle():
            self.windowHandle().setScreen(target_screen)

        self.setGeometry(screen_geometry)
        # Force the window to be positioned correctly, especially for multi-monitor setups
        self.move(screen_geometry.x(), screen_geometry.y())

        self.danmaku_manager: DanmakuManager = DanmakuManager()
        self.setCentralWidget(self.danmaku_manager)

    def add_danmaku(self, model: DanmakuModel) -> None:
        """
        Adds a danmaku to the DanmakuManager associated with this window.

        Args:
            model (DanmakuModel): The danmaku data model to add.
        """
        self.danmaku_manager.add_danmaku(model)