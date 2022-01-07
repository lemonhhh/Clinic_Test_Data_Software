from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import os

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mainLayout()

    def initUI(self):
        self.setWindowTitle("图片")

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  ##浏览器引擎控件
        # url = "http://www.baidu.com"
        # 打开本地html文件#使用绝对地址定位，在地址前面加上 file:/// ，将地址的 \ 改为/
        # self.myHtml.load(QUrl("file:///Users/liumenghan/毕设/my_project/test/try/render.html"))

        # self.myHtml.setUrl(QUrl("http://google.com"))

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bar.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)


        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    ex.show()
    sys.exit(app.exec_())