from __future__ import annotations

from PyQt6.QtCore import QDate, QEvent, QObject, QPoint, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

APP_STYLESHEET = """
QWidget {
    color: #F3E9D8;
    font-family: 'Segoe UI';
    font-size: 11pt;
}
QFrame#OuterFrame {
    background: #17120E;
    border: 1px solid #4A3A2A;
    border-radius: 12px;
}
QFrame#TitleBar {
    background: #241A13;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid #4A3A2A;
}
QLabel#TitleLabel {
    color: #F7EFE3;
    font-size: 10pt;
    font-weight: 600;
}
QFrame#ContentFrame {
    background: #17120E;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
}
QFrame#Card {
    background: #231A14;
    border: 1px solid #4A3A2A;
    border-radius: 10px;
}
QLabel#Heading {
    font-size: 20pt;
    font-weight: 600;
    color: #F9F1E6;
}
QLabel#Subtle {
    color: #C2AC90;
}
QLabel#Field {
    font-weight: 600;
    color: #F4E9D8;
}
QLineEdit, QDateEdit, QComboBox, QListWidget, QCalendarWidget {
    background: #2C2018;
    border: 1px solid #5A4733;
    border-radius: 8px;
    padding: 8px;
    color: #F3E9D8;
}
QDateEdit::drop-down, QComboBox::drop-down {
    border: 0px;
}
QComboBox QAbstractItemView, QListWidget {
    background: #2C2018;
    selection-background-color: #B8863C;
    selection-color: #1A130D;
    border: 1px solid #5A4733;
}
QCalendarWidget QToolButton {
    background: #3A2A1F;
    color: #F3E9D8;
    border: 0;
    border-radius: 6px;
    padding: 6px;
    margin: 2px;
}
QCalendarWidget QToolButton:hover {
    background: #4A3628;
}
QCalendarWidget QSpinBox {
    background: #2C2018;
    color: #F3E9D8;
    border: 1px solid #5A4733;
    border-radius: 6px;
    padding: 4px;
}
QCalendarWidget QMenu {
    background: #2C2018;
    color: #F3E9D8;
}
QCalendarWidget QAbstractItemView:enabled {
    background: #2A1F17;
    color: #F3E9D8;
    selection-background-color: #A33224;
    selection-color: #FFF7EC;
    outline: 0;
    border: 1px solid #5A4733;
    gridline-color: #4A3A2A;
}
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background: #231A14;
    border-bottom: 1px solid #4A3A2A;
}
QPushButton {
    border-radius: 8px;
    padding: 10px 14px;
    border: 0px;
}
QPushButton#Primary {
    background: #A33224;
    color: #FFF2E6;
    font-weight: 600;
}
QPushButton#Primary:hover {
    background: #8D2B1F;
}
QPushButton#Secondary {
    background: #3D2C20;
    color: #F3E9D8;
}
QPushButton#Secondary:hover {
    background: #4A3628;
}
QPushButton#Danger {
    background: #7A1F18;
    color: #FFEDE8;
    font-weight: 600;
}
QPushButton#Danger:hover {
    background: #651912;
}
QPushButton#TitleControl {
    background: transparent;
    color: #F3E9D8;
    border-radius: 0px;
    padding: 7px 12px;
}
QPushButton#TitleControl:hover {
    background: #4A3628;
}
QPushButton#TitleClose:hover {
    background: #A33224;
    color: #FFF2E6;
}
"""


class _TitleDragFilter(QObject):
    def __init__(self, host: QWidget) -> None:
        super().__init__(host)
        self.host = host
        self._drag_active = False
        self._offset = QPoint()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._offset = event.globalPosition().toPoint() - self.host.frameGeometry().topLeft()
            return True

        if event.type() == QEvent.Type.MouseMove and self._drag_active:
            self.host.move(event.globalPosition().toPoint() - self._offset)
            return True

        if event.type() == QEvent.Type.MouseButtonRelease:
            self._drag_active = False
            return True

        return False


def apply_app_style(app: QApplication) -> None:
    app.setStyleSheet(APP_STYLESHEET)


def center_window(widget: QWidget, width: int, height: int) -> None:
    widget.resize(width, height)
    screen = QApplication.primaryScreen()
    if not screen:
        return
    geometry = screen.availableGeometry()
    x = geometry.center().x() - width // 2
    y = geometry.center().y() - height // 2
    widget.move(x, y)


def setup_frameless(widget: QWidget, title: str, content_padding: int = 22) -> QVBoxLayout:
    widget.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)

    root = QVBoxLayout(widget)
    root.setContentsMargins(0, 0, 0, 0)

    outer = QFrame()
    outer.setObjectName("OuterFrame")
    outer_layout = QVBoxLayout(outer)
    outer_layout.setSpacing(0)
    outer_layout.setContentsMargins(0, 0, 0, 0)

    titlebar = QFrame()
    titlebar.setObjectName("TitleBar")
    title_layout = QHBoxLayout(titlebar)
    title_layout.setContentsMargins(8, 0, 0, 0)

    title_label = QLabel(title)
    title_label.setObjectName("TitleLabel")
    title_layout.addWidget(title_label)
    title_layout.addStretch(1)

    min_button = QPushButton("-")
    min_button.setObjectName("TitleControl")
    min_button.clicked.connect(widget.showMinimized)

    close_button = QPushButton("x")
    close_button.setObjectName("TitleControl")
    close_button.setProperty("class", "close")
    close_button.setObjectName("TitleClose")
    close_button.clicked.connect(widget.close)

    title_layout.addWidget(min_button)
    title_layout.addWidget(close_button)

    content = QFrame()
    content.setObjectName("ContentFrame")
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(content_padding, content_padding, content_padding, content_padding)
    content_layout.setSpacing(12)

    outer_layout.addWidget(titlebar)
    outer_layout.addWidget(content)
    root.addWidget(outer)

    drag_filter = _TitleDragFilter(widget)
    titlebar.installEventFilter(drag_filter)
    title_label.installEventFilter(drag_filter)
    widget._title_drag_filter = drag_filter

    return content_layout


def make_card_layout(parent_layout: QVBoxLayout) -> QVBoxLayout:
    card = QFrame()
    card.setObjectName("Card")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(10)
    parent_layout.addWidget(card)
    return layout


def iso_date(qdate: QDate) -> str:
    return qdate.toString("yyyy-MM-dd")
