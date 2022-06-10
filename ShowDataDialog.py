# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import pyqtSlot

from Util.Common import show_error_message

from UI.Ui_ShowDataDialog import Ui_show_data_dialog

import datetime


class ShowDataDialog(QDialog):
    def __init__(self, parent=None,label=None):
        super(ShowDataDialog, self).__init__(parent)

        self.__UI = Ui_show_data_dialog()
        self.__UI.setupUi(self)

        self.set_tableview(self.__UI.tableView, horsize=100, versize=70)
        self.data_model = self.get_model(label)

    # 接收查询结果
    @pyqtSlot(tuple)
    def do_receive_data(self, data_tuple):
        #设置deta_model
        self.data_model = self.add_model_data(self.data_model, list(data_tuple))
        self.set_model()

    # 初始化table_view函数
    def set_tableview(self, widget: QTableView, horsize: int, versize: int, is_altercolor=True) -> None:
        widget.setAlternatingRowColors(is_altercolor)
        widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        widget.setSelectionMode(QAbstractItemView.SingleSelection)
        widget.horizontalHeader().setDefaultSectionSize(horsize)
        widget.verticalHeader().setDefaultSectionSize(versize)
        widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

##  ============================== 功能函数区 ==============================#
    # 获取数据模型
    def get_model(self,label):
        raw_model = self.get_raw_model(labels=label, colCount=len(label))
        return raw_model

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

        # 设置数据模型

    # 设置模型
    def set_model(self):
        if self.data_model is None:
            return
        #将tableView展示出来
        self.__UI.tableView.setModel(self.data_model)

