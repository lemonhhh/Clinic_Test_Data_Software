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
from pyecharts.charts import Pie,Tab



#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class DiseaseClass(QDialog):

    def __init__(self, parent=None):

        #继承所有dialog的方法
        super(DiseaseClass, self).__init__(parent)

        self.chuxue_num=None
        self.xueshuan_num=None
        self.red_num=None
        self.white_num=None
        self.trans_num=None
        self.mix_num=None
        self.a_num=None
        self.b_num=None
        self.xueguan_num=None
        self.t1_num=None
        self.t3_num=None
        self.t2a_num=None
        self.t2b_num=None
        self.t2m_num=None
        self.t2n_num=None

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

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "disease_pie.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    def generate_data(self):
        sql = """select count(*) from Diagnosis_table where binary_type = "出血病" """
        self.cursor.execute(sql)
        self.chuxue_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where binary_type = "血栓病" """
        self.cursor.execute(sql)
        self.xueshuan_num = self.cursor.fetchone()[0]


        #血栓和血管
        #出血病的数量
        sql = """select count(*) from Diagnosis_table where result = "白色血栓" """
        self.cursor.execute(sql)
        self.white_num = self.cursor.fetchone()[0]
        #血栓的数量
        sql = """select count(*) from Diagnosis_table where result = "红色血栓" """
        self.cursor.execute(sql)
        self.red_num = self.cursor.fetchone()[0]

        #血栓的
        sql = """select count(*) from Diagnosis_table where result = "透明血栓" """
        self.cursor.execute(sql)
        self.trans_num = self.cursor.fetchone()[0]

        # 血栓的
        sql = """select count(*) from Diagnosis_table where result = "混合血栓" """
        self.cursor.execute(sql)
        self.mix_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where haemophilia_type = "A" """
        self.cursor.execute(sql)
        self.a_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where haemophilia_type = "B" """
        self.cursor.execute(sql)
        self.b_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where haemophilia_type = "VWD" """
        self.cursor.execute(sql)
        self.xueguan_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "1" """
        self.cursor.execute(sql)
        self.t1_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "3" """
        self.cursor.execute(sql)
        self.t3_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "2A" """
        self.cursor.execute(sql)
        self.t2a_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "2B" """
        self.cursor.execute(sql)
        self.t2b_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "2M" """
        self.cursor.execute(sql)
        self.t2m_num = self.cursor.fetchone()[0]

        sql = """select count(*) from Diagnosis_table where vwd_type = "2N" """
        self.cursor.execute(sql)
        self.t2n_num = self.cursor.fetchone()[0]



    def generate_chart(self):
        tab = Tab()
        tab.add(self.generate_pie([['出血病', self.chuxue_num], ['血栓病', self.xueshuan_num]],"出血/血栓"), "出血/血栓")
        tab.add(self.generate_pie([['红色血栓', self.red_num], ['透明血栓', self.trans_num],['白色血栓',self.white_num],['混合血栓',self.mix_num]],"血栓分类"), "血栓分类")
        tab.add(self.generate_pie([['血友病A', self.a_num], ['血友病B', self.b_num],['血管性血友病',self.xueguan_num]],"血友病"), "血友病")
        tab.add(self.generate_pie([['1', self.t1_num], ['3', self.t3_num], ['2A', self.t2a_num], ['2B', self.t2b_num], ['2M', self.t2m_num], ['2N', self.t2n_num]],"VWD"), "VWD")



        tab.render("disease_pie.html")

    def generate_pie(self,data,title):

        c = (
            Pie()
                .add(
                "类别",
                data,
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
                .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        return c
    def binary_pie(self):
        data = [['出血病', self.chuxue_num], ['血栓病', self.xueshuan_num]]

        c = (
            Pie()
                .add(
                "类别",
                data,
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
        )
        return c

    def thrombosis_pie(self):
        data = [['红色血栓', self.red_num], ['透明血栓', self.trans_num],['白色血栓',self.white_num],['混合血栓',self.mix_num]]
        c = (
            Pie()
                .add("类别", data)
                .set_global_opts(title_opts=opts.TitleOpts(title="血栓分类"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c

    def haemophilia_pie(self):
        data = [['血友病A', self.a_num], ['血友病B', self.b_num],['血管性血友病',self.xueguan_num]]

        c=(
            Pie(init_opts=opts.InitOpts(width="800px", height="500px"))
                .add(
                series_name="血友病",
                data_pair=data,
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

        )
        return c

    def vwd_pie(self):
        data = [['1', self.t1_num], ['3', self.t3_num], ['2A', self.t2a_num], ['2B', self.t2b_num], ['2M', self.t2m_num], ['2N', self.t2n_num]]
        c = (
            Pie()
                .add(
                "VWD类型",
                data,
                radius=["30%", "75%"],
                center=["25%", "50%"],
                rosetype="radius",
                label_opts=opts.LabelOpts(is_show=False),
                )
                .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c



    ##  ============================== 功能函数区 ==============================#

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")


    # 检查查询是否有效
    def is_search_valid(self):
        return True if self.cursor.rowcount != 0 else False

    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))








