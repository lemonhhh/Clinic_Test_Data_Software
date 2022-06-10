# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
#Qt相关
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal,Qt


from UI.Ui_ManDiag import Ui_Dialog


#导入配置文件
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import datetime

class ManDiag(QDialog):

    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    def __init__(self, parent=None,patient_id=None):
        super(ManDiag, self).__init__(parent)
        #初始化ui
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)
        self.__UI.lineEdit_pID.setText(patient_id)


        self.connection = None
        self.cursor = None
        self.logger = None

        self.set_connection_cursor()
        self.set_logger()

        # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

        # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    def get_exam_sql_data(self) -> (str, list):
        sql = None
        #列表
        data_list = []

        patientID = self.__UI.lineEdit_pID.text()
        result = self.__UI.lineEdit_result.text()
        describe = self.__UI.lineEdit_describe.text()


        data_list.append(patientID)
        data_list.append(result)
        data_list.append(describe)



        sql = """UPDATE diagnosis
SET man_result='%s',description='%s'
WHERE patient_ID='%s'""" % (result, describe,patientID)

        sql_patient="""UPDATE patients SET result='是' WHERE patient_ID='%s'"""%patientID


        return sql, sql_patient,data_list

    @pyqtSlot()
    def on_btn_commit_clicked(self):
        sql, sql_patient,data_list = self.get_exam_sql_data()
        if sql is not None:
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                self.cursor.execute(sql_patient)
                self.connection.commit()


                show_successful_message(self, "插入成功")
                # 手动发射信号
                self.data_update_signal.emit(data_list)
            except Exception as e:
                show_error_message(self, "插入错误，请检查")
                self.record_debug(e)
            self.close()