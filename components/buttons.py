from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.display import Display
    from components.info import Info

from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot

from components.variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber


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
    def __init__(self,
                 display: 'Display',
                 info: 'Info',
                 parent: QWidget | None = None,
                 *args, **kwargs
                 ) -> None:

        super().__init__(parent, *args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self.operation = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self) -> str:
        return self._equation

    @equation.setter
    def equation(self, value: str):
        self._equation = value
        self.info.setText(value)

    # funcao que cria meu grid e faz a ligação dos botões
    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    # Para adicionar o qss se o botao nao for numerico ou .
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, columnNumber)

                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)

    # funcao que liga o slot ao botão atraves de click
    def _connectButtonClicked(self, button: Button, slot: Slot):
        button.clicked.connect(slot)

    # funcao que configura o botão para ser especial
    def _configSpecialButton(self, button: Button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)  # type: ignore

        if text in '+-*/':
            self._connectButtonClicked(
                button, self._makeSlot(self._operatorClicked, button)
            )

    # funcao que cria o slot
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    # funcao que insere o valor do botão no display
    def _insertButtonTextToDisplay(self, button: Button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    # funcao que limpa o display
    def _clear(self):
        self.equation = ''
        self._left = None
        self._right = None
        self.operation = None
        self.equation = self._equationInitialValue
        self.display.clear()

    # funcao que faz a logica dos operadores
    def _operatorClicked(self, button: Button):
        buttonText = button.text()  # +-/*
        displaytext = self.display.text()  # numero da esquerda _left
        self.display.clear()

        # se clicar no operador antes de clicar em um número
        if not isValidNumber(displaytext) and self._left is None:
            print("Nao eh valido")
            return

        if self._left is None:
            self._left = displaytext

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
