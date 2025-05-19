from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer

from .get_current_time import get_current_time

class ClockWidget(QLabel):
    """
    A reusable QLabel-based widget that displays the current time
    and updates automatically every second.

    Parameters:
        time_format (str): Custom format string like "HH:mm:SS"
        zone (int or str): UTC offset (int) or pytz timezone string (str)
    """
    def __init__(self, time_format: str = "HH:mm:SS", zone=None, parent=None):
        super().__init__(parent)
        self.time_format = time_format
        self.zone = zone

        # Optional styling
        self.setStyleSheet("font-size: 20px; padding: 5px;")

        # Start timer to update every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)

        # Initial update
        self.update_time()

    def update_time(self):
        info = get_current_time(self.time_format, self.zone)
        self.setText(info["raw"])
