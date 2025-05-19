from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from components.clock.time_utils import get_current_time
from datetime import datetime

class DigitalClockWidget(QLabel):
    """
    A QLabel-based widget that displays the current time,
    updated externally via update(datetime) method.
    """

    def __init__(self, time_format: str = "HH:mm:SS", parent=None):
        super().__init__(parent)
        self.time_format = time_format
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 20px; padding: 5px;")

    def update_info(self, info: dict):
        """
        update the text from the input time info
        """
        self.setText(info["raw"])