from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
import math
from datetime import datetime

class AnalogClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setStyleSheet("background-color: white;")
        # self._time = datetime.utcnow()

    def update_time(self, dt: datetime):
        """Accepts a timezone-aware datetime object and triggers repaint."""
        self._time = dt
        self.update()

    def paintEvent(self, event):
        if not self._time:
            return

        side = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Draw clock face
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#f0f0f0")))
        painter.drawEllipse(-95, -95, 190, 190)

        # Hour marks
        painter.setPen(QPen(Qt.black, 1))
        for i in range(12):
            painter.drawLine(0, -88, 0, -95)
            painter.rotate(30)

        # Draw hands
        self.draw_hand(painter, angle=self._hour_angle(),   length=50, width=6, color="#333")
        self.draw_hand(painter, angle=self._minute_angle(), length=70, width=4, color="#666")
        self.draw_hand(painter, angle=self._second_angle(), length=85, width=2, color="#cc0000")

    def draw_hand(self, painter, angle, length, width, color):
        painter.save()
        painter.setPen(QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap))
        painter.rotate(angle)
        painter.drawLine(0, 0, 0, -length)
        painter.restore()

    def _hour_angle(self):
        return 30 * ((self._time.hour % 12) + self._time.minute / 60)

    def _minute_angle(self):
        return 6 * (self._time.minute + self._time.second / 60)

    def _second_angle(self):
        return 6 * self._time.second
