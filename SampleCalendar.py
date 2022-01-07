# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
from datetime import date
import random

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Pie, Calendar


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class SampleCalendar(QDialog):

    def __init__(self, parent=None):

        # 继承所有dialog的方法
        super(SampleCalendar, self).__init__(parent)

        self.initUI()
        # 在这里写查询吧
        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()
        self.set_logger()


        self.data = []
        self.generate_data()
        # 生成html
        self.generate_chart()

        self.mainLayout()

    def initUI(self):
        self.setWindowTitle("每日入库样本")
        self.setMinimumSize(1300, 800)

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  # 浏览器引擎控件

        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "calendar_heatmap.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    def generate_data(self):
        begin = datetime.date(2021, 11, 10)
        end = date.today()

        for i in range((end - begin).days + 1):
            this_date = str(begin + datetime.timedelta(days=i))
            count_sql = """SELECT COUNT(*) FROM(select date_format(creation_date, '%%Y-%%m-%%d') as dates from t_sample) tmp WHERE tmp.dates = '%s' """ % this_date
            self.cursor.execute(count_sql)
            this_count = self.cursor.fetchone()[0]
            self.data.append([this_date,this_count])


    def generate_chart(self):

        c = (
    Calendar(
        init_opts=opts.InitOpts(
            width="1000px",
            height="1000px")) .add(
                series_name="",
                yaxis_data=self.data,
                calendar_opts=opts.CalendarOpts(
                    pos_top="120",
                    pos_left="30",
                    pos_right="30",
                    range_="2022",
                    yearlabel_opts=opts.CalendarYearLabelOpts(
                        is_show=True),
                ),
    ) .set_global_opts(
        title_opts=opts.TitleOpts(
            pos_top="30",
            pos_left="center",
            title="每日入库情况"),
        visualmap_opts=opts.VisualMapOpts(
            max_=20,
            min_=0,
            orient="horizontal",
            pos_top= "top",
            is_piecewise=False),
    ) .render("calendar_heatmap.html"))
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
