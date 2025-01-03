from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget


from components.variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty


class Button(QPushButton):
    def __init__(self, text: str, parent: QPushButton | None = None,
                 *args, **kwargs) -> None:
        super().__init__(text, parent, *args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]

        self._makeGrid()

    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    # Para adicionar o qss se o botao nao for numerico ou .
                    button.setProperty("cssClass", "specialButton")

                self.addWidget(button, rowNumber, columnNumber)
