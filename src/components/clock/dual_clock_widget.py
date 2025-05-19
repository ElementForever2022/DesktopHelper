from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
from .analog_clock_widget import AnalogClockWidget
from .digital_clock_widget import DigitalClockWidget
from .time_utils import get_current_time

class DualClockWidget(QWidget):
    """
    Composite widget that displays both a digital and analog clock,
    synchronized with the same timezone and refresh interval.
    """
    def __init__(self, time_format: str = "YYYY-MM-DD HH:mm:SS", zone=None, parent=None):
        super().__init__(parent)
        self.time_format = time_format
        self.zone = zone

        self.digital_clock_widget = DigitalClockWidget(time_format=self.time_format)
        self.analog_clock_widget = AnalogClockWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.digital_clock_widget)
        layout.addWidget(self.analog_clock_widget)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)
        self.update_time()

    def update_time(self):
        info = get_current_time(self.time_format, self.zone)
        self.digital_clock_widget.update_info(info)
        self.analog_clock_widget.update_time(info["datetime"])

    def set_timezone(self, zone):
        """Dynamically update timezone."""
        self.zone = zone
        self.update_time()
