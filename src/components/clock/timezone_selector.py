from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout
from PySide6.QtCore import Signal
import pytz

class TimezoneSelector(QWidget):
    """
    A simple dropdown widget that allows the user to select a timezone.
    
    Emits:
        timezone_changed(str): emitted when the selected timezone changes
    """
    timezone_changed = Signal(str)

    def __init__(self, parent=None, default_tz: str = "UTC"):
        super().__init__(parent)

        self.combo = QComboBox()
        self.combo.addItems(pytz.all_timezones)
        self.combo.setCurrentText(default_tz)

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        self.setLayout(layout)

        self.combo.currentTextChanged.connect(self.timezone_changed.emit)

    def current_timezone(self) -> str:
        return self.combo.currentText()
