from PyQt5.QtGui import QFont

class DanmakuModel:
    def __init__(self, text, color="#FFFFFF", size=20, speed=300, font_family="Microsoft YaHei", font_weight=QFont.Normal, font_style=QFont.StyleNormal, text_decoration=""):
        self.text = text
        self.color = color
        self.size = size
        self.speed = speed
        self.font_family = font_family
        self.font_weight = font_weight
        self.font_style = font_style
        self.text_decoration = text_decoration