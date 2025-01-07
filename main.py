from pathlib import Path
import sys

from PySide6.QtGui import QIcon
import ctypes
from PySide6.QtWidgets import QApplication

from components.variables import WINDOW_ICON_PATH
from components.mainWindow import MainWindow
from components.display import Display
from components.info import Info
from components.buttons import ButtonsGrid
from styles import setupTheme


# Função para configurar o ícone do aplicativo
def configure_icon(app: QApplication, icon_path: Path):
    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)  # Configura o ícone global para o aplicativo

    # Configurações específicas para Windows
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "my_unique_app_id")
        ctypes.windll.user32.LoadIconW(0, str(icon_path))

    return icon


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme(app, theme="dark")

    # Configura o ícone global e do processo
    icon = configure_icon(app, WINDOW_ICON_PATH)

    # Cria a janela principal
    window = MainWindow()
    # Configura o ícone da janela retornado pela função
    window.setWindowIcon(icon)

    # Info
    info = Info('sua conta')
    window.addWidgetVertical(info)

    # Dislay
    display = Display()
    display.setPlaceholderText("Digite algo")
    window.addWidgetVertical(display)

    # Grid Button
    buttonsGrid = ButtonsGrid(display, info, window)
    window.verticalLayout.addLayout(buttonsGrid)

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
