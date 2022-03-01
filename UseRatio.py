# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

#pyecharts
import pyecharts.options as opts
from pyecharts.charts import TreeMap

#模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class UseRatio(QDialog):

    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(UseRatio, self).__init__(parent)
        #初始化
        self.initUI()

        # 在这里写查询吧
        self.logger = None
        self.connection = None
        self.cursor = None
        # 建立连接
        self.set_connection_cursor()
        self.set_logger()


        #生成数据
        self.generate_data()

        #生成html
        self.generate_chart()

        self.mainLayout()


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

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "treemap.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)


        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    def generate_data(self):

        #冰箱-层-架子-抽屉-盒子-试管
        #冰箱
        sql_refrigerator = """select distinct (refrigerator) from positions """
        self.cursor.execute(sql_refrigerator)
        refrigerator_tuple = self.cursor.fetchall()
        refrigerator_list = ([j for i in list(refrigerator_tuple) for j in i])
        #层
        sql_layer = """select distinct (layer) from positions """
        self.cursor.execute(sql_layer)
        layer_tuple = self.cursor.fetchall()
        layer_list = ([j for i in list(layer_tuple) for j in i])
        #架子
        sql_shelf = """select distinct (shelf) from positions """
        self.cursor.execute(sql_shelf)
        shelf_tuple = self.cursor.fetchall()
        shelf_list = ([j for i in list(shelf_tuple) for j in i])
        #抽屉
        sql_drawer = """select distinct (drawer) from positions """
        self.cursor.execute(sql_drawer)
        drawer_tuple = self.cursor.fetchall()
        drawer_list = ([j for i in list(drawer_tuple) for j in i])

        #盒子
        sql_box = """select distinct (box) from positions """
        self.cursor.execute(sql_box)
        box_tuple = self.cursor.fetchall()
        box_list = ([j for i in list(box_tuple) for j in i])

        self.tree_map_data = []
        for a in refrigerator_list:
            #value
            sql_all = """select count(*) from positions where refrigerator='%s' """ % (a)
            self.cursor.execute(sql_all)
            number_all = self.cursor.fetchone()[0]
            #使用的
            sql_use = """select count(*) from positions where refrigerator='%s' and flag=1""" % (a)
            self.cursor.execute(sql_use)
            number_use = self.cursor.fetchone()[0]
            number_ratio = number_use / number_all * 100
            self.tree_map_data.append({"name": a, "value":number_ratio,"children":[]})


        for second_layer in self.tree_map_data:
            last_name = second_layer['name']
            data = second_layer['children']
            for b in layer_list:
                sql_all = """select count(*) from positions where refrigerator='%s'and layer='%s' """ % (last_name,b)
                self.cursor.execute(sql_all)
                number_all = self.cursor.fetchone()[0]
                # 使用的
                sql_use = """select count(*) from positions where refrigerator='%s' and layer='%s'and flag=1""" % (last_name,b)
                self.cursor.execute(sql_use)
                number_use = self.cursor.fetchone()[0]
                number_ratio = number_use / number_all * 100
                data.append({"name": b, "value":number_ratio,"children":[]})

            for third_layer in data:
                second_name = third_layer['name']
                data_third = third_layer['children']
                for c in shelf_list:
                    sql_all = """select count(*) from positions where refrigerator='%s'and layer='%s'and shelf='%s' """ % (
                    last_name, second_name,c)
                    self.cursor.execute(sql_all)
                    number_all = self.cursor.fetchone()[0]
                    # 使用的
                    sql_use = """select count(*) from positions where refrigerator='%s' and layer='%s' and shelf='%s' and flag=1""" % (
                    last_name,second_name,c)
                    self.cursor.execute(sql_use)
                    number_use = self.cursor.fetchone()[0]
                    number_ratio = number_use / number_all * 100
                    data_third.append({"name": c, "value": number_ratio, "children": []})

                for forth_layer in data_third:
                    third_name = forth_layer['name']
                    data_forth = forth_layer['children']
                    for d in drawer_list:
                        sql_all = """select count(*) from positions where refrigerator='%s'and layer='%s'and shelf='%s' and drawer='%s' """ % (
                            last_name, second_name, third_name,d)
                        self.cursor.execute(sql_all)
                        number_all = self.cursor.fetchone()[0]
                        # 使用的
                        sql_use = """select count(*) from positions where refrigerator='%s' and layer='%s' and shelf='%s' and drawer='%s' and flag=1""" % (
                            last_name, second_name, third_name,d)
                        self.cursor.execute(sql_use)
                        number_use = self.cursor.fetchone()[0]
                        number_ratio = number_use / number_all * 100
                        data_forth.append({"name": d, "value": number_ratio, "children": []})

                    for fifth_layer in data_forth:
                        forth_name = fifth_layer['name']
                        data_fifth = fifth_layer['children']
                        for e in box_list:
                            sql_all = """select count(*) from positions where refrigerator='%s'and layer='%s'and shelf='%s' and drawer='%s' and box='%s' """ % (
                                last_name, second_name, third_name,forth_name,e)
                            self.cursor.execute(sql_all)
                            number_all = self.cursor.fetchone()[0]
                            # 使用的
                            sql_use = """select count(*) from positions where refrigerator='%s' and layer='%s' and shelf='%s' and drawer='%s' and box='%s' and flag=1""" % (
                                last_name, second_name, third_name, forth_name,e)
                            self.cursor.execute(sql_use)
                            number_use = self.cursor.fetchone()[0]
                            number_ratio = number_use / number_all * 100
                            data_fifth.append({"name": e, "value": number_ratio, "children": []})




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




