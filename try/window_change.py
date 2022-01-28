import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QPushButton
from Ui_logging import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot

app = QApplication(sys.argv)

class Logging(QMainWindow):
    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        print(self.height)
        print(self.width)

        self.resize(600,600)
        self.btn = QPushButton("你好",self)
        self.btn.clicked.connect(self.cao)

    def cao(self):
        print("ye")
        # self.btn.setVisible(False)
        self.__UI = Ui_MainWindow()
        self.__UI.setupUi(self)
        self.btn.setVisible(False)
        self.btn.deleteLater()


window = Logging()
window.show()

# Start the event loop.
app.exec()
