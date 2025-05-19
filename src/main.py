import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, QDateTime, Qt

from components.clock.clock_widget import ClockWidget
from components.clock.analog_clock import AnalogClock
from components.clock.timezone_selector import TimezoneSelector

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
        
        # Create time label
        self.clock_label = ClockWidget(time_format="YYYY-MM-DD HH:mm:SS", zone="Asia/Tokyo")
        self.analog_clock = AnalogClock()
        self.tz_selector = TimezoneSelector(default_tz="Asia/Shanghai")
        
        self.tz_selector.timezone_changed.connect(lambda tz: setattr(self.clock_label, "zone", tz))
        self.tz_selector.timezone_changed.connect(lambda tz: setattr(self.analog_clock, "zone", tz))
        
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.clock_label)
        layout.addWidget(self.analog_clock)
        layout.addWidget(self.tz_selector)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_dialog(self):
        QMessageBox.information(self, "inform", "Hello, World")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopHelper()
    window.show()
    sys.exit(app.exec())