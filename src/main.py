import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, QDateTime, Qt
import tzlocal
# from components.clock.clock_widget import ClockWidget
# from components.clock.analog_clock import AnalogClock
from components.clock.timezone_selector import TimezoneSelector
from components.clock.dual_clock_widget import DualClockWidget

class DesktopHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.init_timer()

    def init_ui(self):
        self.setWindowTitle("Desktop Helper")
        self.setGeometry(100, 100, 300, 200)

        # Create button
        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.show_dialog)
        
        # Create time components
        self.local_timezone = str(tzlocal.get_localzone()) # str format of LOCAL timezone e.g."Asia/Tokyo"
        self.tz_selector = TimezoneSelector(default_tz=self.local_timezone)
        self.dual_clock_widget = DualClockWidget(time_format="YYYY-MM-DD HH:mm:SS", zone=self.local_timezone)
        self.tz_selector.timezone_changed.connect(self.dual_clock_widget.set_timezone)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tz_selector)
        layout.addWidget(self.dual_clock_widget)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_dialog(self):
        QMessageBox.information(self, "inform", "Hello, World")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopHelper()
    window.show()
    sys.exit(app.exec())