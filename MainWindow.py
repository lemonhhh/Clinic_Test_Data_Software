# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot
from UI.Ui_MainWindow import Ui_MainWindow
from CreateSample import CreateSample
from RecycleBinDialog import RecycleBinDialog
from Util.Common import get_sql_connection, show_error_message, get_logger
from SearchWindow import SearchWindow

import sys
import datetime
from qt_material import apply_stylesheet


# 主窗口
class MainWindow(QMainWindow):
    #初始化函数
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__UI = Ui_MainWindow()
        self.__UI.setupUi(self)
        self.setCentralWidget(self.__UI.tabWidget)
        self.setGeometry(200, 200, 1100, 800)
        #设置右侧tab的宽度
        self.set_tableview(self.__UI.tableView_show, horsize=130, versize=50)
        #设置model
        self.data_model = self.get_model()
        self.set_model()
        self.location = ""

##  ============================== 自动连接槽函数区 ==============================#
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.on_act_search_triggered()

    def on_search_sample_clicked(self):
        self.on_act_search_triggered()

    @pyqtSlot()
    def on_add_sample_clicked(self):
        self.on_act_create_triggered()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.on_act_recyclebin_triggered()

    @pyqtSlot()
    def on_trash_clicked(self):
        self.on_act_recyclebin_triggered()

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_treeWidget_show_currentItemChanged(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):  ##目录树节点变化
        flg = False
        #表示已经到最后一级了
        if current.childCount() == 0:
            flg = True

        #是当前选中的widget
        first_name = current.text(0)

        #递归地找到路径
        while current.parent() is not None:
            current = current.parent()
            first_name = current.text(0) + '-' +  first_name

        self.data_model = self.get_raw_model(labels=['样本编号', '姓名', '样本类型',
                                               '样本量', '添加日期', '更新时间', '状态', '归属'], colCount=8)
        #连接到数据库
        connection = get_sql_connection()
        #创建游标
        cursor = connection.cursor()
        if flg:
            print("first name",first_name)
            sql = """select * from t_sample where t_sample.sample_belong = '%s' """ % first_name
            print(sql)
        else:
            sql = """select * from t_sample where t_sample.sample_belong like '""" + first_name + """%'"""
        cursor.execute(sql)
        if self.__UI.tableView_show.model() is not None:
            self.__UI.tableView_show.model().clear()

        if cursor.rowcount != 0:
            print("sss")
            self.data_model = self.add_model_data(self.data_model, list(cursor.fetchall()))
            self.set_model()
        self.location = first_name


    #点击【新增】选项槽函数
    @pyqtSlot()
    def on_act_create_triggered(self):


        creation_dialog = CreateSample(self,self.location)

        creation_dialog.setAttribute(Qt.WA_DeleteOnClose)
        #连接槽函数
        creation_dialog.data_update_signal.connect(self.do_receive_data)
        creation_dialog.show()



    # 点击【查询】槽函数
    @pyqtSlot()
    def on_act_search_triggered(self):
        search_dialog = SearchWindow(self)
        search_dialog.setAttribute(Qt.WA_DeleteOnClose)
        search_dialog.show()

    # 点击【回收站】槽函数
    @pyqtSlot()
    def on_act_recyclebin_triggered(self):
        recycle_dialog = RecycleBinDialog(self)
        recycle_dialog.setAttribute(Qt.WA_DeleteOnClose)
        recycle_dialog.show()
##  ===========================================================================#

##  ============================== 自定义槽函数区 ==============================#
    @pyqtSlot(list)
    def do_receive_data(self, data_list: list):
        self.data_model = self.add_model_data(self.data_model, data_list)

##  ===========================================================================#

##  ============================== 功能函数区 ==============================#
    # 获取数据模型
    def get_model(self):
        raw_model = self.get_raw_model(labels=['样本编号', '姓名', '样本类型',
                                               '样本量', '添加日期', '更新时间', '状态', '归属'], colCount=8)
        #从数据库中得到所有的数据
        data_list = self.read_sql_data()

        if len(data_list) > 0:
            return self.add_model_data(raw_model, data_list)

    #获取无数据的数据模型
    def get_raw_model(self, labels: list, colCount: int =2) -> QStandardItemModel:
        '''
        获取无数据的数据模型
        :param colCount:要设置的列数
        :return:无数据的数据模型
        '''
        raw_model = QStandardItemModel(0, colCount)
        raw_model.setHorizontalHeaderLabels(labels)
        return raw_model

    # 读取数据库数据
    def read_sql_data(self) -> list:
        #获取数据库的连接
        connection = get_sql_connection()
        #建立游标
        cursor = connection.cursor()
        #执行sql语句
        cursor.execute('select * from t_sample;')
        #返回全部内容
        return cursor.fetchall()

    # 向模型添加数据
    def add_model_data(self, model: QStandardItemModel, data_list: list) -> QStandardItemModel:
        fun = self.choose_add_function(data_list)
        if fun is None:
            show_error_message(self, "数据类型错误,请检查")
            return

        final_model = fun(model, data_list)

        return final_model

    # 生产者函数：选择添加模式
    def choose_add_function(self, data_list: list):
        method = None

        if isinstance(data_list[0], tuple):
            method = self.add_multiple_data
        else:
            method = self.add_single_data

        return method

    # 添加单条记录
    def add_single_data(self, model: QStandardItemModel, record: list) -> QStandardItemModel:
        return model.appendRow([QStandardItem(self.process_data(item)) for item in record])

    # 添加多条信息
    def add_multiple_data(self, model: QStandardItemModel, data_list: list) -> QStandardItemModel:
        for record in data_list:
            row = []
            for item in record:
                item = self.process_data(item)
                row.append(QStandardItem(item))

            model.appendRow(row)

        return model

    # 处理数据
    def process_data(self, data: any) -> any:
        if isinstance(data, str):
            pass
        elif isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data = str(data)

        return data

    # 初始化table_view函数
    def set_tableview(self, widget: QTableView, horsize: int, versize: int, is_altercolor=True) -> None:
        widget.setAlternatingRowColors(is_altercolor)
        widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        widget.setSelectionMode(QAbstractItemView.SingleSelection)
        widget.horizontalHeader().setDefaultSectionSize(horsize)
        widget.verticalHeader().setDefaultSectionSize(versize)
        widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 设置数据模型
    def set_model(self):
        if self.data_model is None:
            return
        self.__UI.tableView_show.setModel(self.data_model)

##  =======================================================================#


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # apply_stylesheet(app, theme='dark_teal.xml')
    win.showFullScreen()
    win.show()
    sys.exit(app.exec())