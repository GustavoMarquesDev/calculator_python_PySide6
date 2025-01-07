from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurando o layout base
        self.centralWidget_ = QWidget()
        self.verticalLayout = QVBoxLayout(self.centralWidget_)
        self.centralWidget_.setLayout(self.verticalLayout)
        self.setCentralWidget(self.centralWidget_)
        self.setWindowTitle("Calculator")

    # Para setar um tamnho fixo para a janela, após abrir ela nao muda

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetVertical(self, widget: QWidget):
        self.verticalLayout.addWidget(widget)

    # metodo que cria uma caixa de mensagem
    def makeMessageBox(self):
        return QMessageBox(self)
