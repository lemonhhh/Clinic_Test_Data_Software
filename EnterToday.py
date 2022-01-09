# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import datetime

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

#模块
from ShowDataDialog import ShowDataDialog
from Util.Common import get_sql_connection, get_logger, show_error_message

#导入ui
from UI.Ui_EnterTodayDialog import Ui_enter_today_dialog
from UI.Ui_SearchWindow import Ui_Dialog






class EnterToday(QDialog):
    data_signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(EnterToday, self).__init__(parent)
        #设置ui
        self.__UI = Ui_enter_today_dialog()
        self.__UI.setupUi(self)

        ##自定义的方法##
        # 设置model_view
        self.set_tableview(self.__UI.tableView, horsize=100, versize=200)

        # 设置数据模型
        self.data_model = self.get_model()

        #在这里写查询吧
        self.logger = None
        self.connection = None
        self.cursor = None

        self.set_connection_cursor()
        self.set_logger()

        #获取sql的内容
        self.sql = self.get_search_sql()

        if self.sql is not None:
            try:
                self.cursor.execute(self.sql)  # 执行sql语句
                self.show_search_data()
            except Exception as e:
                self.record_debug(e)
                show_error_message(self, '查询失败')





    # 接收查询结果
    @pyqtSlot(tuple)
    def do_receive_data(self, data_tuple):
        #将数据模型更新为添加数据之后的
        self.data_model = self.add_model_data(self.data_model, list(data_tuple))
        #将数据模型应用到view上
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

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    # 获得查询语句
    def get_search_sql(self) -> str:
        sql = None
        #今日日期
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")

        sql = """select * from t_sample where t_sample.creation_date like '%%%%%s%%%%' """ % today_date
        return sql


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


    # 检查查询是否有效
    def is_search_valid(self):
        return True if self.cursor.rowcount != 0 else False

    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))


    # 获取（原始）数据模型
    def get_model(self):
        #传入标签的名称和数量
        raw_model = self.get_raw_model(labels=['样本编号', '姓名', '样本类型',
                                               '样本量', '添加日期', '更新时间', '状态', '归属','位置','是否有检查结果'], colCount=10)
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
        #处理日期格式的
        elif isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data = str(data)

        return data



    # 设置模型
    def set_model(self):
        if self.data_model is None:
            return

        self.__UI.tableView.setModel(self.data_model)

