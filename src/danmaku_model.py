from PyQt5.QtGui import QFont
import uuid

class DanmakuModel:
    """
    Represents the data model for a single danmaku message.
    Stores properties like text, color, size, speed, and font details.
    """
    def __init__(self, 
                 text: str, 
                 color: str = "#FFFFFF", 
                 size: int = 20, 
                 speed: int = 300, 
                 font_family: str = "Microsoft YaHei", 
                 font_weight: int = QFont.Normal, # Using QFont.Weight type for clarity
                 font_style: QFont.Style = QFont.StyleNormal, # Using QFont.Style type
                 text_decoration: str = "") -> None:
        """
        Initializes a DanmakuModel instance.

        Args:
            text (str): The text content of the danmaku.
            color (str, optional): The color of the danmaku text. Defaults to "#FFFFFF" (white).
            size (int, optional): The font size of the danmaku. Defaults to 20.
            speed (int, optional): The speed at which the danmaku moves across the screen. Defaults to 300.
            font_family (str, optional): The font family for the danmaku text. Defaults to "Microsoft YaHei".
            font_weight (int, optional): The font weight (e.g., QFont.Normal, QFont.Bold). Defaults to QFont.Normal.
            font_style (QFont.Style, optional): The font style (e.g., QFont.StyleNormal, QFont.StyleItalic). Defaults to QFont.StyleNormal.
            text_decoration (str, optional): Text decoration (e.g., "underline"). Defaults to "".
        """
        self.text: str = text
        self.color: str = color
        self.size: int = size
        self.speed: int = speed
        self.font_family: str = font_family
        self.font_weight: int = font_weight # QFont.Weight is an enum, typically int
        self.font_style: QFont.Style = font_style # QFont.Style is an enum
        self.text_decoration: str = text_decoration
        self.danmaku_id: str = str(uuid.uuid4())