# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
#Qt相关
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal,Qt

#加载UI
from UI.Ui_CreateSampleWindow import Ui_Dialog
from UI.Ui_InsertResult import Ui_Dialog_exam


#导入配置文件
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import datetime

class InsertExam(QDialog):

    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    def __init__(self, parent=None,sample_id=None,patient_id=None):
        super(InsertExam, self).__init__(parent)
        #初始化ui
        self.__UI = Ui_Dialog_exam()
        self.__UI.setupUi(self)
        #todo:
        #这里要完善，需要获取到
        self.__UI.lineEdit_sampleID.setText(sample_id)
        self.__UI.lineEdit_patientID.setText(patient_id)


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
        #检查编号
        examID = self.__UI.lineEdit_examID.text()
        #病人编号
        patientID = self.__UI.lineEdit_patientID.text()
        #样本编号
        sampleID = self.__UI.lineEdit_sampleID.text()
        #aptt
        aptt = self.__UI.value_aptt.value()
        #pt
        pt = self.__UI.value_pt.value()
        #tt
        tt = self.__UI.value_tt.value()
        #fib
        fib = self.__UI.value_fib.value()

        data_list.append(examID)
        data_list.append(patientID)
        data_list.append(sampleID)
        data_list.append(pt)
        data_list.append(aptt)
        data_list.append(tt)
        data_list.append(fib)

        #定义sql语句
        if examID != '' and patientID != '':
            sql = """insert into exam_result(exam_ID,sample_ID,patient_ID,pt,aptt,tt,fib) 
            values('%s','%s','%s',%f,'%f','%f','%f')""" % (examID, sampleID,patientID,pt,aptt,tt,
                                                            fib)
        print(sql)
        return sql, data_list

    @pyqtSlot()
    def on_btn_exam_clicked(self):
        sql,  data_list = self.get_exam_sql_data()
        if sql is not None:
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                self.connection.commit()
                show_successful_message(self, "插入成功")
                # 手动发射信号
                self.data_update_signal.emit(data_list)
            except Exception as e:
                show_error_message(self, "插入错误，请检查")
                self.record_debug(e)
            self.close()