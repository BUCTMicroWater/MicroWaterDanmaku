from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QFont
from websockets.sync.server import serve
import json
from .danmaku_model import DanmakuModel

class DanmakuSource(QThread):
    danmakuSignal = pyqtSignal(object)

    def run(self):
        def echo(websocket):
            for message in websocket:
                try:
                    parsed = json.loads(message)
                    model = DanmakuModel(
                        text=parsed.get('text', ''),
                        color=parsed.get('color', '#FFFFFF'),
                        size=parsed.get('size', 20),
                        speed=parsed.get('speed', 300),
                        font_family=parsed.get('fontFamily', "Microsoft YaHei"),
                        font_weight=parsed.get('fontWeight', QFont.Normal),
                        font_style=parsed.get('fontStyle', QFont.StyleNormal),
                        text_decoration=parsed.get('textDecoration', "")
                    )
                    self.danmakuSignal.emit(model)
                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Error processing message: {e}")  # Handle errors

        with serve(echo, "localhost", 3210) as server:
            server.serve_forever()