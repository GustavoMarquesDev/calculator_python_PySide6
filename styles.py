import qdarkstyle
from PySide6.QtWidgets import QApplication

from variables import (
    DARK_COLOR, DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR, BACKGROUND_COLOR,
    SECONDARY_BACKGROUND_COLOR, HOVER_COLOR, BORDER_COLOR, PRESSED_COLOR
)

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {DARK_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR}; 
    }}
"""

light_qss = f"""
    QWidget {{
        background: #ffffff;
        color: #000000;
    }}
    QPushButton {{
        background-color: {SECONDARY_BACKGROUND_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: {HOVER_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {PRESSED_COLOR};
    }}
    QLineEdit {{
        background: {BACKGROUND_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 3px;
    }}
"""


def setupTheme(app: QApplication, theme="dark"):
    if theme == "dark":
        # Estilo escuro com qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet() + qss)
    elif theme == "light":
        # Estilo claro
        app.setStyleSheet(light_qss + qss)
