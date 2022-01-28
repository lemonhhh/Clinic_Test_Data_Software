from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys


class Screen(QMainWindow):
    def __init__(self):
        super(Screen, self).__init__()
        self.initUI()

    def initUI(self):
        self.lightsBtn = QPushButton('Turn On')
        self.lightsBtn.setCheckable(True)
        self.lightsBtn.setStyleSheet(
            "QPushButton:checked {color: white; background-color: red;}")
        self.lightsBtn.clicked.connect(self.lightsBtnHandler)

        # probaply you will want to set self.lightsBtn
        # at certain spot using layouts
        self.setCentralWidget(self.lightsBtn)

    def lightsBtnHandler(self):
        if self.lightsBtn.isChecked():
            self.turnOnLights()
        else:
            self.turnOffLights()

    def turnOnLights(self):
        print("truned on")

    def turnOffLights(self):
        print("truned off")


app = QApplication(sys.argv)
window = Screen()
window.show()
sys.exit(app.exec_())
