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
from pyecharts.charts import TreeMap

#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class UseRatio(QDialog):

    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(UseRatio, self).__init__(parent)
        self.initUI()
        self.mainLayout()

        self.tree_map_data = []
        #生成数据
        # self.generate_data()
        #生成html
        # self.generate_chart()

        #在这里写查询吧
        self.logger = None
        self.connection = None
        self.cursor = None
        #建立连接
        self.set_connection_cursor()
        self.set_logger()






    def initUI(self):
        self.setWindowTitle("使用率统计")
        self.setMinimumSize(1000,800)

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)

        # 网页嵌入PyQt5
        self.myHtml = QWebEngineView()  ##浏览器引擎控件


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "echarts_option_query.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)


        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    # def generate_data(self):
    #     pass
    #     #几层
    #     #冰箱-层-架子-抽屉-盒子-试管
    #     sql_refrigerator = """select distinct (refrigerator) from positions """
    #     refrigerator_cursor = self.connection.cursor()
    #     refrigerator_list =
    #     layer_list =
    #     for a in refrigerator_list:
    #         value = 使用率 = count(flag=1) / count(总数)
    #         self.tree_map_data.append({"name":,"value":,"children":[]})
    #         for b in layer_list:
    #             a-b组合的使用率
    #             count(总数) = select count(*) from positions where refrigerator=a and layer=b
    #             count(用过的) = select count(*) from positions where refrigerator=a and layer=b and flag=1
    #             value = 使用率 =
    #             for c in shelf_list:
    #                 for d in drawer_list:
    #                     for e in box_list:






    # if self.sql is not None:
    #     try:
    #         self.cursor.execute(self.sql)  # 执行sql语句
    #         self.show_search_data()
    #     except Exception as e:
    #         self.record_debug(e)
    #         show_error_message(self, '查询失败')

    def generate_chart(self):
        (
            TreeMap(init_opts=opts.InitOpts(width="1200px", height="720px"))
                .add(
                series_name="option",
                data=self.tree_map_data,
                visual_min=300,
                leaf_depth=1,
                # 标签居中为 position = "inside"
                label_opts=opts.LabelOpts(position="inside"),
            )
                .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
                title_opts=opts.TitleOpts(
                    title="使用率统计", subtitle="使用率统计", pos_left="leafDepth"
                ),
            )
                .render("treemap.html")
        )

    # 接收查询结果
    @pyqtSlot(tuple)
    def do_receive_data(self, data_tuple):
        #将数据模型更新为添加数据之后的
        self.data_model = self.add_model_data(self.data_model, list(data_tuple))
        #将数据模型应用到view上
        self.set_model()



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

    def create_show_dialog(self):
        self.data_signal.connect(self.do_receive_data)



    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))




