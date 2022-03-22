# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json


from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Boxplot
from pyecharts.charts import Pie

from pyecharts.charts import Bar
from pyecharts.faker import Faker

# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class PatientStatis(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(PatientStatis, self).__init__(parent)
        # 初始化ui
        self.initUI()
        # 为查询进行配置
        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()

    def initUI(self):
        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)
        btn1 = QPushButton("性别")
        btn2 = QPushButton("年龄")
        btn3 = QPushButton("是否有诊断结果")
        btn4 = QPushButton("是否吸烟")
        btn5 = QPushButton("是否饮酒")
        btn6 = QPushButton("是否有输血史")
        btn7 = QPushButton("是否有传染你病史")
        btn8 = QPushButton("是否有过敏史")


        hlayout = QHBoxLayout()

        hlayout.addWidget(btn1)
        hlayout.addWidget(btn2)
        hlayout.addWidget(btn3)
        hlayout.addWidget(btn4)
        hlayout.addWidget(btn5)
        hlayout.addWidget(btn6)
        hlayout.addWidget(btn7)
        hlayout.addWidget(btn8)

        hwidget = QWidget(self)
        hwidget.setLayout(hlayout)

        btn1.clicked.connect(self.sta_gender)
        btn2.clicked.connect(self.sta_age)
        btn3.clicked.connect(self.sta_result)
        btn4.clicked.connect(self.sta_smoke)


        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.move(10, 50)
        self.myHtml.resize(1000, 600)
        self.myHtml.setVisible(False)

    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)


    def sta_gender(self):
        self.myHtml.setVisible(True)

        #有多少女
        sql_f = """SELECT COUNT(*) FROM Patient_table WHERE gender='女'"""
        self.cursor.execute(sql_f)
        num_f = self.cursor.fetchone()[0]
        #有多少男
        sql_m = """SELECT COUNT(*) FROM Patient_table WHERE gender='男'"""
        self.cursor.execute(sql_m)
        num_m = self.cursor.fetchone()[0]

        x_data = ["女", "男"]
        y_data = [num_f,num_m]

        (
            Pie(init_opts=opts.InitOpts(width="800px", height="500px"))
                .add(
                series_name="性别分布",
                data_pair=[list(z) for z in zip(x_data, y_data)],
                radius=["50%", "70%"],
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
                .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
                .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                # label_opts=opts.LabelOpts(formatter="{b}: {c}")
            )
                .render("gender_sta.html")
        )
        self.load_url("gender_sta.html")


    def sta_age(self):
        self.myHtml.setVisible(True)

        #0-10
        sql1 = """select count(*) from Patient_table where (age>0 and age<=10)"""
        self.cursor.execute(sql1)
        num1 = self.cursor.fetchone()[0]

        sql2 = """select count(*) from Patient_table where (age>10 and age<=20)"""
        self.cursor.execute(sql2)
        num2 = self.cursor.fetchone()[0]

        sql3 = """select count(*) from Patient_table where (age>20 and age<=30)"""
        self.cursor.execute(sql3)
        num3 = self.cursor.fetchone()[0]

        sql4 = """select count(*) from Patient_table where (age>30 and age<=40)"""
        self.cursor.execute(sql4)
        num4 = self.cursor.fetchone()[0]

        sql5 = """select count(*) from Patient_table where (age>40 and age<=50)"""
        self.cursor.execute(sql5)
        num5 = self.cursor.fetchone()[0]

        sql6 = """select count(*) from Patient_table where (age>50 and age<=60)"""
        self.cursor.execute(sql6)
        num6 = self.cursor.fetchone()[0]

        sql7 = """select count(*) from Patient_table where (age>60 and age<=70)"""
        self.cursor.execute(sql7)
        num7 = self.cursor.fetchone()[0]

        sql8 = """select count(*) from Patient_table where (age>70 and age<=80)"""
        self.cursor.execute(sql8)
        num8 = self.cursor.fetchone()[0]

        sql9 = """select count(*) from Patient_table where (age>80 and age<=90)"""
        self.cursor.execute(sql9)
        num9 = self.cursor.fetchone()[0]

        sql10 = """select count(*) from Patient_table where (age>90)"""
        self.cursor.execute(sql10)
        num10 = self.cursor.fetchone()[0]

        data_x = ['0','10','20','30','40','50','60','70','80','90以上']
        data_y = [num1,num2,num3,num4,num5,num6,num7,num8,num9,num10]


        c = (
            Bar()
                .add_xaxis(data_x)
                .add_yaxis("年龄分布", data_y, color=Faker.rand_color())
                .set_global_opts(
                title_opts=opts.TitleOpts(title="年龄分布"),
                datazoom_opts=opts.DataZoomOpts(orient="vertical"),
            )
                .render("patient_age.html")
        )

        self.load_url("patient_age.html")

    def sta_result(self):
        self.myHtml.setVisible(True)
        # 有多少女
        sql_yes = """SELECT COUNT(*) FROM Patient_table WHERE result='有'"""
        self.cursor.execute(sql_yes)
        num_yes = self.cursor.fetchone()[0]

        sql_no = """SELECT COUNT(*) FROM Patient_table WHERE result='无'"""
        self.cursor.execute(sql_no)
        num_no = self.cursor.fetchone()[0]

        x_data = ["有", "无"]
        y_data = [num_yes, num_no]

        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(x_data, y_data)],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
                .set_global_opts(title_opts=opts.TitleOpts(title="是否有诊断结果"))
                .render("result_sta_pie.html")
        )
        self.load_url("result_sta_pie.html")

    def sta_smoke(self):
        self.myHtml.setVisible(True)
        # 有多少女
        sql_yes = """SELECT COUNT(*) FROM Patient_table WHERE smoke='有'"""
        self.cursor.execute(sql_yes)
        num_yes = self.cursor.fetchone()[0]

        sql_no = """SELECT COUNT(*) FROM Patient_table WHERE smoke='否'"""
        self.cursor.execute(sql_no)
        num_no = self.cursor.fetchone()[0]

        sql_null = """SELECT COUNT(*) FROM Patient_table WHERE smoke='未知'"""
        self.cursor.execute(sql_null)
        num_null = self.cursor.fetchone()[0]

        x_data = ["是", "否","未知"]
        y_data = [num_yes, num_no,num_null]

        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(x_data, y_data)],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
                .set_global_opts(title_opts=opts.TitleOpts(title="是否有吸烟史"))
                .render("result_sta_pie.html")
        )
        self.load_url("result_sta_pie.html")





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
