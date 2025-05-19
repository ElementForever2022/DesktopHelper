import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, QDateTime

from components.clock.clock_widget import ClockWidget

class DesktopAssistant(QWidget):
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
        clock_label = ClockWidget(time_format="YYYY-MM-DD HH:mm:SS", zone="Asia/Tokyo")

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(clock_label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_dialog(self):
        QMessageBox.information(self, "inform", "Hello, World")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopAssistant()
    window.show()
    sys.exit(app.exec())