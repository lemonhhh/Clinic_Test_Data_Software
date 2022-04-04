# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
import numpy as np

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton,QLabel,QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

#作图相关
import pyecharts.options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Line


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class DataChange(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(DataChange, self).__init__(parent)
        # 为查询进行配置
        self.db_list = []

        self.dict = {"APTT":"APTT","Ag":"Ag","全血凝固时间":"Act","血浆蛋白":"RIPA","凝血因子活性":"FV3C","结合胆红素":"CB","PP":"pp","血糖":"BS"}

        self.age_list = []
        self.gender_list = []

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()


        # 初始化ui
        self.initUI()




    def initUI(self):
        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)

        #输入病人ID
        self.label1 = QLabel("输入病人ID",self)
        self.label1.move(10,10)
        self.line1 = QLineEdit(self)
        self.line1.move(150,10)

        self.label2 = QLabel("请输入要观察的指标",self)
        self.label2.move(10,40)
        self.cb = QComboBox(self)
        self.cb.addItems(["APTT", "Ag", "全血凝固时间","血浆蛋白","凝血因子活性","结合胆红素","PP","血糖"])
        self.cb.move(150,40)

        self.btn = QPushButton("确定", self)
        self.btn.move(10,70)
        self.btn.clicked.connect(self.ShowChange)  # 绑定槽函数，确定后，显示后续所有ui


        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.move(10, 120)
        self.myHtml.resize(1000, 600)


    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

    def ShowChange(self):
        time_list = []
        data_list = []
        #生成数据
        pID = self.line1.text()
        project = self.dict[self.cb.currentText()]
        sql = """select %s,add_date from Exam_table where patient_ID='%s' """ % (project,pID)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for i in data:
            time_list.append(i[1])
            data_list.append(i[0])

        print(time_list)
        print(data_list)

        (
            Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
                .add_xaxis(xaxis_data=time_list)
                .add_yaxis(
                series_name="指标变化",
                y_axis=data_list,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="指标变化"),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            )
                .render("data_change.html")
        )
        self.load_url("data_change.html")




##  ============================== 功能函数区 ==============================#

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
