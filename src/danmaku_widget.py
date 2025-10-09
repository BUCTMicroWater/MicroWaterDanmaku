from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QWidget # Added QWidget for parent type hint
from PyQt5.QtCore import QPoint, QPropertyAnimation, QAbstractAnimation, pyqtBoundSignal
from PyQt5.QtGui import QFont, QColor, QShowEvent # Added QShowEvent for type hinting
from .danmaku_signal import danmaku_signal
from .danmaku_model import DanmakuModel # Added for type hinting

class DanmakuWidget(QLabel):
    """
    Represents a single danmaku message as a QLabel widget.
    Handles its appearance, animation, and deletion.
    """
    def __init__(self, model: DanmakuModel, parent: QWidget, start_pos: QPoint, end_pos: QPoint) -> None:
        """
        Initializes a DanmakuWidget.

        Args:
            model (DanmakuModel): The data model for the danmaku.
            parent (QWidget): The parent widget for this danmaku.
            start_pos (QPoint): The starting position for the animation.
            end_pos (QPoint): The ending position for the animation.
        """
        super().__init__(model.text, parent)
        self.model: DanmakuModel = model
        self.danmaku_id: str = model.danmaku_id
        self.start_pos: QPoint = start_pos
        self.end_pos: QPoint = end_pos
        self.animation: QPropertyAnimation | None = None # Initialize animation attribute
        

        font = QFont(model.font_family)
        font.setPointSize(model.size)
        font.setWeight(model.font_weight)
        # QFont.Style is an enum, ensure model.font_style is compatible or cast
        font.setStyle(QFont.Style(model.font_style) if isinstance(model.font_style, int) else model.font_style)
        self.setFont(font)

        style_sheet = f"color: {model.color};"
        if model.text_decoration:
             style_sheet += f" text-decoration: {model.text_decoration};" # Added space before text-decoration
        self.setStyleSheet(style_sheet)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 200)) # Black shadow with some transparency
        self.setGraphicsEffect(shadow)

        self.adjustSize()

    def showEvent(self, event: QShowEvent) -> None:
        """
        Handles the show event of the widget.
        Starts the danmaku animation when the widget is shown.

        Args:
            event (QShowEvent): The show event.
        """
        super().showEvent(event)
        self.move(self.start_pos)
        self.animation = QPropertyAnimation(self, b"pos")
        # Ensure speed is not zero to avoid division by zero
        duration = int(1000 * self.parent().width() / self.model.speed) if self.model.speed > 0 else 10000
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.start_pos)
        self.animation.setEndValue(self.end_pos)
        self.animation.finished.connect(self.on_animation_finished)
        self.animation.start()
        
        # Connect to delete signal
        danmaku_signal.danmaku_signal_delete.connect(self.check_delete)
        
    def on_animation_finished(self) -> None:
        """
        Called when the danmaku animation finishes.
        Disconnects the delete signal, emits a signal that this danmaku is finished,
        and schedules the widget for deletion.
        """
        try:
            # Disconnect signal to prevent memory leaks
            danmaku_signal.danmaku_signal_delete.disconnect(self.check_delete)
        except TypeError: # Signal might have already been disconnected
            pass 
        danmaku_signal.danmaku_signal_delete.emit(self.danmaku_id) # Emit signal that this danmaku is done
        self.deleteLater()
        
    def check_delete(self, danmaku_id: str) -> None:
        """
        Checks if this danmaku instance needs to be deleted based on the provided ID.
        If the ID matches, it stops the animation (if running), disconnects the signal,
        hides the widget, and schedules it for deletion.

        Args:
            danmaku_id (str): The ID of the danmaku to check for deletion.
        """
        # Check if this is the danmaku to be deleted
        if danmaku_id == self.danmaku_id:
            # Stop animation if it's running
            if self.animation and self.animation.state() == QAbstractAnimation.Running:
                self.animation.stop()
            
            try:
                # Disconnect signal to prevent memory leaks
                danmaku_signal.danmaku_signal_delete.disconnect(self.check_delete)
            except TypeError: # Signal might have already been disconnected
                pass
            # Hide to remove immediately from view
            self.hide()
            # Delete self
            self.deleteLater()