# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot

from UI.Ui_MainWindow import Ui_MainWindow
#
# 导入各种类
from CreateSample import CreateSample
from RecycleBinDialog import RecycleBinDialog
from EnterToday import EnterToday
from SearchWindow import SearchWindow
from SampleClass import SampleClass
from UseRatio import UseRatio
from SampleCalendar import SampleCalendar


from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message


import sys
import datetime
from qt_material import apply_stylesheet


# 主窗口
class MainWindow(QMainWindow):
    # 初始化函数
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__UI = Ui_MainWindow()
        self.__UI.setupUi(self)

        self.setCentralWidget(self.__UI.tabWidget)
        self.setGeometry(200, 200, 1100, 800)

        # 设置右侧tab的宽度
        self.set_tableview(self.__UI.tableView_show, horsize=130, versize=50)
        # 设置model
        self.data_model = self.get_model()
        self.set_model()

        # 自己设置的
        self.location = ""
        self.sample_id = ""


##  ============================== 自动连接槽函数区 ==============================#
    # 查询
    @pyqtSlot()
    def on_search_sample_clicked(self):
        self.on_act_search_triggered()

    # 新增样本
    @pyqtSlot()
    def on_add_sample_clicked(self):
        self.on_act_create_triggered()

    # 删除样本
    @pyqtSlot()
    def on_delete_sample_clicked(self):
        self.on_act_delete_triggered()

    # 查看回收站样本
    @pyqtSlot()
    def on_trash_clicked(self):
        self.on_act_recyclebin_triggered()

    # 当日入库
    @pyqtSlot()
    def on_enter_today_clicked(self):
        self.on_act_look_today_triggered()

    # 样本类别
    @pyqtSlot()
    def on_sample_class_clicked(self):
        self.on_act_sample_class_triggered()

    @pyqtSlot()
    def on_use_ratio_clicked(self):
        self.on_act_compute_use_triggered()

    @pyqtSlot()
    def on_calendar_clicked(self):
        self.on_act_calendar_triggered()


    # 槽函数
    def talbe_choose(self):
        row = (self.__UI.tableView_show.currentIndex().row())
        id_data = (self.data_model.itemData(self.data_model.index(row, 0)))
        self.sample_id = (id_data[0])


    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    # 目录树节点变化
    def on_treeWidget_show_currentItemChanged(
            self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        flg = False
        # 表示已经到最后一级了
        if current.childCount() == 0:
            flg = True

        # 是当前选中的widget
        first_name = current.text(0)

        # 递归地找到路径
        while current.parent() is not None:
            current = current.parent()
            first_name = current.text(0) + '-' + first_name

        self.data_model = self.get_raw_model(
            labels=[
                '样本编号',
                '姓名',
                '样本类型',
                '样本量',
                '添加日期',
                '更新时间',
                '状态',
                '归属',
                '位置',
                '是否有检查结果'],
            colCount=10)
        # 连接到数据库
        connection = get_sql_connection()
        # 创建游标
        cursor = connection.cursor()

        #已经到最后一级
        if flg:
            sql = """select * from t_sample where t_sample.sample_belong = '%s' """ % first_name
        else:
            sql = """select * from t_sample where t_sample.sample_belong like '""" + \
                first_name + """%'"""
        # 执行查询结果
        cursor.execute(sql)

        if self.__UI.tableView_show.model() is not None:
            self.__UI.tableView_show.model().clear()

        if cursor.rowcount != 0:
            self.data_model = self.add_model_data(
                self.data_model, list(cursor.fetchall()))
            self.set_model()
        # 传入的参数
        self.location = first_name


##  ============================== 槽函数区 ==============================#


    # 点击【新增】选项槽函数
    @pyqtSlot()
    def on_act_create_triggered(self):
        creation_dialog = CreateSample(self, self.location)
        creation_dialog.setAttribute(Qt.WA_DeleteOnClose)
        # 连接槽函数
        creation_dialog.data_update_signal.connect(self.do_receive_data)
        creation_dialog.show()

    # 点击【查询】槽函数
    @pyqtSlot()
    def on_act_search_triggered(self):
        search_dialog = SearchWindow(self)
        search_dialog.setAttribute(Qt.WA_DeleteOnClose)
        search_dialog.show()

    # 点击【删除】槽函数
    def on_act_delete_triggered(self):
        sample_id = self.sample_id
        sql_find = """select * from t_sample where ID=%s """ % (sample_id)
        connection_find = get_sql_connection()
        cursor_find = connection_find.cursor()
        cursor_find.execute(sql_find)
        data_find = cursor_find.fetchone()
        ID = data_find[0]
        name = data_find[1]
        type = data_find[2]
        sample_size = data_find[3]
        creation_date = data_find[4]
        modification_date = data_find[5]
        sample_status = '回收站'
        sample_belong = data_find[7]
        box_loc = data_find[8]
        result_flag = data_find[9]

        # sql_insert = """insert into recycle_sample(ID,name,type,sample_size,creation_date, modification_date,sample_status, sample_belong,box,result)
        #     values('%s','%s','%s',%f,'%s','%s','%s', '%s','%s','%s')""" % (ID, name, type, sample_size, creation_date,
        #                                                                    modification_date, sample_status, sample_belong, box_loc, result_flag)
        # connection_insert = get_sql_connection()
        # cursor_insert = connection_insert.cursor()
        # cursor_insert.execute(sql_insert)
        # connection_insert.commit()

        #删除
        sql = """delete from t_sample where ID=%s """ % (sample_id)
        print("delete sql is ")
        print(sql)

        connection_delete = get_sql_connection()
        cursor_delete = connection_delete.cursor()

        if sql is not None:
            try:
                # 执行sql语句
                cursor_delete.execute(sql)
                # 提交结果
                connection_delete.commit()
                show_successful_message(self, "删除成功")
                # 手动发射信号

            except Exception as e:
                show_error_message(self, "删除错误，请检查")

    # 点击【回收站】槽函数
    @pyqtSlot()
    def on_act_recyclebin_triggered(self):
        recycle_dialog = RecycleBinDialog(self)
        recycle_dialog.setAttribute(Qt.WA_DeleteOnClose)
        recycle_dialog.show()

    # 点击【今日入库】槽函数
    def on_act_look_today_triggered(self):
        today_dialog = EnterToday(self)
        today_dialog.setAttribute(Qt.WA_DeleteOnClose)
        today_dialog.show()

    # 点击【样本类别】槽函数
    def on_act_sample_class_triggered(self):
        sample_class_widget = SampleClass(self)
        # sample_class_widget.setAttribute(Qt.WA_DeleteOnClose)
        sample_class_widget.show()


    # 点击【样本类别】槽函数
    @pyqtSlot()
    def on_act_compute_use_triggered(self):
        ratio_dialog = UseRatio(self)
        ratio_dialog.setAttribute(Qt.WA_DeleteOnClose)
        ratio_dialog.show()

        # 点击【样本类别】槽函数
    @pyqtSlot()
    def on_act_calendar_triggered(self):
        calender_dialog = SampleCalendar(self)
        calender_dialog.setAttribute(Qt.WA_DeleteOnClose)
        calender_dialog.show()
##  ===========================================================================#

##  ============================== 自定义槽函数区 ==============================#

    @pyqtSlot(list)
    def do_receive_data(self, data_list: list):
        self.data_model = self.add_model_data(self.data_model, data_list)

##  ===========================================================================#

##  ============================== 功能函数区 ==============================#
    # 获取数据模型
    def get_model(self):
        raw_model = self.get_raw_model(
            labels=[
                '样本编号',
                '姓名',
                '样本类型',
                '样本量',
                '添加日期',
                '更新时间',
                '状态',
                '归属',
                '位置',
                '是否有检查结果'],
            colCount=10)
        # 从数据库中得到所有的数据
        data_list = self.read_sql_data()

        if len(data_list) > 0:
            return self.add_model_data(raw_model, data_list)

    # 获取无数据的数据模型
    def get_raw_model(
            self,
            labels: list,
            colCount: int = 2) -> QStandardItemModel:
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
        # 获取数据库的连接
        connection = get_sql_connection()
        # 建立游标
        cursor = connection.cursor()
        # 执行sql语句
        cursor.execute('select * from t_sample;')
        # 返回全部内容
        return cursor.fetchall()

    # 向模型添加数据
    def add_model_data(self, model: QStandardItemModel,
                       data_list: list) -> QStandardItemModel:
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
    def add_single_data(self, model: QStandardItemModel,
                        record: list) -> QStandardItemModel:
        return model.appendRow(
            [QStandardItem(self.process_data(item)) for item in record])

    # 添加多条信息
    def add_multiple_data(
            self,
            model: QStandardItemModel,
            data_list: list) -> QStandardItemModel:
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
    def set_tableview(
            self,
            widget: QTableView,
            horsize: int,
            versize: int,
            is_altercolor=True) -> None:
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
