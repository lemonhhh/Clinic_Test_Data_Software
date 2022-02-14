# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Tree


#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class DiseaseTree(QDialog):

    def __init__(self, parent=None):

        #继承所有dialog的方法
        super(DiseaseTree, self).__init__(parent)

        self.initUI()
        # 在这里写查询吧

        # 生成html
        self.generate_chart()
        self.mainLayout()




    def initUI(self):
        self.setWindowTitle("疾病介绍")
        self.setMinimumSize(1000,800)

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  ##浏览器引擎控件

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tree_layout.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)




    def generate_chart(self):
        with open("disease.json", "r", encoding="utf-8") as f:
            j = json.load(f)
        c = (
            Tree()
                # .add("", [j], collapse_interval=2, layout="radial")
                .add("", [j])
                .set_global_opts(title_opts=opts.TitleOpts(title="血液疾病介绍"))
                .render("tree_layout.html")
        )

    ##  ============================== 功能函数区 ==============================#

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")




    def show_search_data(self):
        if self.is_search_valid():
            data_tuple = self.cursor.fetchall()
            self.create_show_dialog()

            #发出信号，参数是发射的内容
            self.data_signal.emit(data_tuple)

        else:
            show_error_message(self, "没有查找到任何结果")




    # 检查查询是否有效
    def is_search_valid(self):
        return True if self.cursor.rowcount != 0 else False

    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))




    # 处理数据
    def process_data(self, data: any) -> any:
        if isinstance(data, str):
            pass
        #处理日期格式的
        elif isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data = str(data)

        return data





