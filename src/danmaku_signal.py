from PyQt5.QtCore import QObject, pyqtSignal
from typing import Any # For pyqtSignal(object)

class DanmakuSignal(QObject):
    """
    Defines global signals for danmaku operations.
    This allows different components of the application to communicate
    events like adding or deleting danmakus.
    """
    # Signal emitted when a new danmaku should be added.
    # The 'object' type can be replaced with DanmakuModel if it's always the type.
    danmaku_signal_add: pyqtSignal = pyqtSignal(object) # Consider using a more specific type if possible, e.g., DanmakuModel
    
    # Signal emitted when a danmaku should be deleted.
    # The argument is the ID (str) of the danmaku to be deleted.
    danmaku_signal_delete: pyqtSignal = pyqtSignal(str)

# Global instance of the DanmakuSignal class for application-wide use.
danmaku_signal: DanmakuSignal = DanmakuSignal()