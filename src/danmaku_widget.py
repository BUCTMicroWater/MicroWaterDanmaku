from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPoint, QPropertyAnimation
from PyQt5.QtGui import QFont, QColor

class DanmakuWidget(QLabel):
    def __init__(self, model, parent, start_pos, end_pos):
        super().__init__(model.text, parent)
        self.model = model
        self.start_pos = start_pos
        self.end_pos = end_pos

        font = QFont(model.font_family)
        font.setPointSize(model.size)
        font.setWeight(model.font_weight)
        font.setStyle(model.font_style)
        self.setFont(font)

        style_sheet = f"color: {model.color};"
        if model.text_decoration:
             style_sheet += f"text-decoration: {model.text_decoration};"
        self.setStyleSheet(style_sheet)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 200)) # Black shadow with some transparency
        self.setGraphicsEffect(shadow)

        self.adjustSize()


    def showEvent(self, event):
        super().showEvent(event)
        self.move(self.start_pos)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(int(1000 * self.parent().width() / self.model.speed))
        self.animation.setStartValue(self.start_pos)
        self.animation.setEndValue(self.end_pos)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()