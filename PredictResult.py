# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
import numpy as np


from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Gauge
from pyecharts.commons.utils import JsCode



#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class PredictResult(QDialog):

    def __init__(self, parent=None,data=None,title=None):

        #继承所有dialog的方法
        super(PredictResult, self).__init__(parent)

        self.initUI()

        self.data = []
        self.data.append(data)
        self.title=title

        # 生成html
        print(self.data)
        print(type(self.data))

        self.generate_chart(data)
        self.mainLayout()


    def initUI(self):
        self.setWindowTitle("风险预测")
        self.setMinimumSize(800,600)

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  ##浏览器引擎控件

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "predict_gauge.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    def generate_chart(self,result):
        result = np.round(result * 100,2)
        (
            Gauge(init_opts=opts.InitOpts(width="800", height="400px"))
                .add(series_name="新冠预测", data_pair=[["", result]])
                .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
                tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{a} <br/>{b} : {c}%"),
            )
                .set_series_opts(
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=[[0.3, "#67e0e3"], [0.7, "#37a2da"], [1, "#fd666d"]], width=30
                    )
                )
            )
                .render("predict_gauge.html")
        )













