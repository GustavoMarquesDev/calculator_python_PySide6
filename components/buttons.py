from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.display import Display
    from components.info import Info
    from components.mainWindow import MainWindow


import math

from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QApplication
from PySide6.QtCore import Slot

from components.variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, converToNumber
from styles import setupTheme


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
                 window: 'MainWindow',
                 parent: QWidget | None = None,
                 app: QApplication | None = None,
                 *args, **kwargs
                 ) -> None:

        super().__init__(parent, *args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['⇅',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = '0'
        self._left = None
        self._right = None
        self.operation = None
        self.app = app
        self.tema = 'dark'

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self) -> str:
        return self._equation

    @equation.setter
    def equation(self, value: str):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._configRightOp)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    # Para adicionar o qss se o botao nao for numerico ou .
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, columnNumber)

                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    # funcao que liga o slot ao botão atraves de click
    def _connectButtonClicked(self, button: Button, slot: Slot):
        button.clicked.connect(slot)

    # funcao que configura o botão para fazer ações
    def _configSpecialButton(self, button: Button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)  # type: ignore

        if text == '◀':
            self._connectButtonClicked(
                button, self.display.backspace)  # type: ignore

        if text in '+-*/^':
            self._connectButtonClicked(
                button, self._makeSlot(self._configLeftOp, text)
            )

        if text == '=':
            self._connectButtonClicked(
                button, self._configRightOp)  # type: ignore

        if text == '⇅':
            self._connectButtonClicked(
                button, self._changeTheme)  # type: ignore

    # funcao que cria o slot
    @Slot()  # type: ignore
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    # funcao que insere o valor do botão no display
    @Slot()  # type: ignore
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    # funcao que limpa o display
    @Slot()
    def _clear(self):
        self.equation = ''
        self._left = None
        self._right = None
        self.operation = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    # funcao que faz a logica dos operadores
    @Slot()  # type: ignore
    def _configLeftOp(self, text):
        displaytext = self.display.text()  # numero da esquerda _left
        self.display.clear()  # limpa o display
        self.display.setFocus()

        # se clicar no operador antes de clicar em um número
        if not isValidNumber(displaytext) and self._left is None:
            self._showError("Digite um número antes")
            return

        if self._left is None:
            self._left = float(displaytext)

            if self._left.is_integer():
                self._left = int(self._left)

        self._op = text
        self.equation = f'{self._left} {self._op} ...'

    # função que executa a operação final do valor da direita com o =
    @Slot()
    def _configRightOp(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta.')
            return

        self._right = converToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = converToNumber(str(round(result, 2)))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisão por zero.')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    # função que mostra uma caixa de mensagem
    def _showError(self, text):
        msgBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        # msgBox.setInformativeText("""
        # It is a long established fact that a reader will be distracted by the
        # readable content of a page when looking at its layout. The point of using
        # Lorem Ipsum is that it has a more-or-less normal distribution of letters,
        # as opposed to using 'Content here, content here', making it look like
        # readable English. Many desktop publishing packages and web page editors
        # """)

        # msgBox.setStandardButtons(
        #     msgBox.StandardButton.Cancel |
        #     msgBox.StandardButton.Ok |
        #     msgBox.StandardButton.Save
        # )

        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.setWindowTitle('Warning')
        msgBox.exec()
        self.display.setFocus()

    # função que muda o tema
    def _changeTheme(self):
        if self.tema == 'dark':
            setupTheme(self.app, theme='light')  # type: ignore
            self.tema = 'light'
        else:
            setupTheme(self.app, theme='dark')  # type: ignore
            self.tema = 'dark'
        self.display.setFocus()
