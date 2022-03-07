#使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from Util.Common import get_sql_connection, get_logger, show_error_message

from UI.Ui_PatientSearch import Ui_Dialog

from ShowDataDialog import ShowDataDialog

import sys


class PatientSearch(QDialog):
    #信号的参数是tuple类型
    data_signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(PatientSearch, self).__init__(parent)
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)

        self.logger = None
        self.connection = None
        self.cursor = None

        self.set_connection_cursor()
        self.set_logger()

##  ============================== 自动连接槽函数区 ==============================#
    # 单击【查询按钮槽函数】
    @pyqtSlot()
    def on_btn_search_clicked(self):
        sql = self.get_search_sql()
        if sql is not None:
            try:
                print("sql here",sql)
                self.cursor.execute(sql)  # 执行sql语句
                label = [
                    '病人编号',
                    '病人姓名',
                    '年龄',
                    '性别',
                    '联系方式',
                    '是否有诊断结果',
                    '是否吸烟',
                    '是否饮酒',
                    '是否有输血史',
                    '是否有手术史',
                    '是否有传染疾病史',
                    '是否过敏史',
                ]
                self.show_search_data(label)

            except Exception as e:
                self.record_debug(e)
                show_error_message(self, '查询失败')

##  ===========================================================================#

##  ============================== 功能函数区 ==============================#
    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    # 获得查询语句
    def get_search_sql(self) -> str:

        sql = None

        pname = self.__UI.lineEdit_name.text()
        pID = self.__UI.lineEdit_pID.text()
        sID = self.__UI.lineEdit_sID.text()
        eID = self.__UI.lineEdit_eID.text()


        if pname:
            #按照姓名查找
            sql = """select * from Patient_table where name = '%s'""" % pname
        if pID:
            sql = """select * from Patient_table where patient_ID = '%s'""" % pID
        if sID:
            #根据sID找到pID
            sql = """SELECT Patient_table.* FROM Patient_table,t_sample WHERE Patient_table.patient_ID=t_sample.patient_ID AND t_sample.ID='%s' """ % sID
        if eID:
            #根据eID找到pID
            sql = """SELECT Patient_table.* FROM Patient_table,Exam_table WHERE Patient_table.patient_ID=Exam_table.patient_ID AND Exam_table.exam_ID='%s'"""  % eID

        print("sql is ",sql)
        return sql

    # 显示查询结果
    def show_search_data(self,label):
        if self.is_search_valid():

            data_tuple = self.cursor.fetchall()
            self.create_show_dialog(label)
            #发出信号，参数是发射的内容
            self.data_signal.emit(data_tuple)

        else:
            show_error_message(self, "没有查找到任何结果")

    # 创建展示窗口
    def create_show_dialog(self,label):
        show_data_dialog = ShowDataDialog(self,label)
        show_data_dialog.setAttribute(Qt.WA_DeleteOnClose)
        #连接信号和槽
        self.data_signal.connect(show_data_dialog.do_receive_data)
        show_data_dialog.show()

    # 检查查询是否有效
    def is_search_valid(self):
        return True if self.cursor.rowcount != 0 else False

    # 记录Debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
##  =======================================================================#

