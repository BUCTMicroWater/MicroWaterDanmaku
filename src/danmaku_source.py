from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont
from websockets.sync.server import serve, ServerConnection # Added for type hinting
import json
from .danmaku_model import DanmakuModel
from .danmaku_signal import danmaku_signal
from typing import Any # For WebSocket handler

class DanmakuSource(QThread):
    """
    A QThread that runs a WebSocket server to receive danmaku messages.
    It parses incoming messages, creates DanmakuModel instances,
    and emits a signal to add the danmaku.
    """
    def __init__(self) -> None:
        """
        Initializes the DanmakuSource thread.
        """
        super().__init__()

    def run(self) -> None:
        """
        The main execution method of the thread.
        Starts a WebSocket server and listens for incoming messages.
        Processes valid messages into DanmakuModel objects and signals their addition.
        """
        def echo(websocket: ServerConnection) -> None: # Added type hint for websocket
            """
            Handles incoming WebSocket messages.

            Args:
                websocket (ServerConnection): The WebSocket connection object.
            """
            for message in websocket:
                try:
                    # Ensure message is treated as string if it's bytes
                    if isinstance(message, bytes):
                        message_str = message.decode('utf-8')
                    else:
                        message_str = str(message) # Ensure it's a string

                    parsed: dict[str, Any] = json.loads(message_str)
                    model = DanmakuModel(
                        text=str(parsed.get('text', '')),
                        color=str(parsed.get('color', '#FFFFFF')),
                        size=int(parsed.get('size', 20)),
                        speed=int(parsed.get('speed', 300)),
                        font_family=str(parsed.get('fontFamily', "Microsoft YaHei")),
                        font_weight=int(parsed.get('fontWeight', QFont.Normal)),
                        font_style=parsed.get('fontStyle', QFont.StyleNormal), # QFont.Style is an enum, usually int
                        text_decoration=str(parsed.get('textDecoration', ""))
                    )
                    danmaku_signal.danmaku_signal_add.emit(model)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON message: {message_str}, Error: {e}")
                except (KeyError, ValueError) as e: # Added ValueError for int conversions
                    print(f"Error processing message content: {parsed if 'parsed' in locals() else message_str}, Error: {e}")
                except Exception as e: # Catch any other unexpected errors
                    print(f"An unexpected error occurred while processing message: {message_str if 'message_str' in locals() else message}, Error: {e}")


        # The 'serve' function from 'websockets' library typically returns a context manager.
        # We assume 'server' object has a 'serve_forever' method.
        with serve(echo, "localhost", 3210) as server:
            print("Danmaku WebSocket server started on localhost:3210") # Added server start message
            server.serve_forever()