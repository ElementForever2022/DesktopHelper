from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
import math

class AnalogClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setStyleSheet("background-color: white;")
        
        # Timer to refresh every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def paintEvent(self, event):
        now = QTime.currentTime()
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Draw clock face
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#f0f0f0")))
        painter.drawEllipse(-95, -95, 190, 190)

        # Draw hour markers
        painter.setPen(QPen(Qt.black, 1))
        for i in range(12):
            painter.drawLine(0, -88, 0, -95)
            painter.rotate(30)

        # Hour hand
        hour_angle = 30 * (now.hour() % 12 + now.minute() / 60.0)
        self.draw_hand(painter, angle=hour_angle, length=50, width=6, color="#333")

        # Minute hand
        minute_angle = 6 * (now.minute() + now.second() / 60.0)
        self.draw_hand(painter, angle=minute_angle, length=70, width=4, color="#666")

        # Second hand
        second_angle = 6 * now.second()
        self.draw_hand(painter, angle=second_angle, length=85, width=2, color="#cc0000")

    def draw_hand(self, painter, angle, length, width, color):
        painter.save()
        painter.setPen(QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap))
        painter.rotate(angle)
        painter.drawLine(0, 0, 0, -length)
        painter.restore()
