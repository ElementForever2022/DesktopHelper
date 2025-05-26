from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from datetime import datetime

class AnalogClockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self._time = datetime.now()
        self._style = "light"  # initial style (will be updated)

    def update_time(self, dt: datetime):
        """
        Receives a timezone-aware datetime and updates both time and style.
        """
        self._time = dt
        hour = dt.hour
        # Define day: 6am–6pm
        self._style = "light" if 6 <= hour < 18 else "dark"
        self.update()
        
    

    def paintEvent(self, event):
        if not self._time:
            return

        side = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Choose style based on time
        if self._style == "light":
            bg_color = QColor("#f0f0f0")
            hour_color = "#333"
            min_color = "#666"
            sec_color = "#cc0000"
            tick_color = Qt.black
        else:
            bg_color = QColor("#1e1e1e")
            hour_color = "#bbbbbb"
            min_color = "#888888"
            sec_color = "#ff5555"
            tick_color = QColor("#aaaaaa")

        # Draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawEllipse(-95, -95, 190, 190)

        # Hour ticks
        painter.setPen(QPen(tick_color, 1))
        for i in range(12):
            painter.drawLine(0, -88, 0, -95)
            painter.rotate(30)

        # Draw hands
        self.draw_hand(painter, self._hour_angle(),   50, 6, hour_color)
        self.draw_hand(painter, self._minute_angle(), 70, 4, min_color)
        self.draw_hand(painter, self._second_angle(), 85, 2, sec_color)

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
