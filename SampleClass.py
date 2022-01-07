# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker

#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class SampleClass(QDialog):

    def __init__(self, parent=None):

        #继承所有dialog的方法
        super(SampleClass, self).__init__(parent)

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
        self.setWindowTitle("样本类别")
        self.setMinimumSize(1000,800)

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  ##浏览器引擎控件


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "pie_rich_label.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)



    def generate_data(self):
        #血浆的数量
        sql1 = """select count(*) from t_sample where t_sample.type = "血浆" """
        cursor1 = self.connection.cursor()
        cursor1.execute(sql1)
        xuejiang = cursor1.fetchone()[0]
        #血细胞
        sql2 ="""select count(*) from t_sample where t_sample.type = "血细胞" """
        cursor2= self.connection.cursor()
        cursor2.execute(sql2)
        cell = cursor2.fetchone()[0]
        self.data = [['血浆',xuejiang],['血细胞',cell]]
        print(self.data)





    # if self.sql is not None:
    #     try:
    #         self.cursor.execute(self.sql)  # 执行sql语句
    #         self.show_search_data()
    #     except Exception as e:
    #         self.record_debug(e)
    #         show_error_message(self, '查询失败')

    def generate_chart(self):
        data = [list(z) for z in zip(Faker.choose(), Faker.values())]
        print(data)
        c = (
            Pie()
                .add(
                "样本类别",
                self.data,
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
                .set_global_opts(title_opts=opts.TitleOpts(title="样本类别"))
                .render("pie_rich_label.html")
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





