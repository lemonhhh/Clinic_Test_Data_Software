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

#检查结果
class InsertExam(QDialog):

    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    def __init__(self, parent=None):
        super(InsertExam, self).__init__(parent)
        #初始化ui
        self.__UI = Ui_Dialog_exam()
        self.__UI.setupUi(self)

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


# 添加新样品类
class CreateSample(QDialog):
    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    #把当前位置location串进来了
    def __init__(self, parent=None,location=None):
        super(CreateSample, self).__init__(parent)
        #ui初始化
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)
        #初始化sql相关
        self.connection = None
        self.cursor = None
        self.logger = None
        self.set_connection_cursor()
        self.set_logger()
        self.location = location

    # 单击【提交】按钮槽函数
    @pyqtSlot()
    def on_btn_commit_clicked(self):
        sql, sql_position,data_list = self.get_insert_sql_data()
        if sql is not None:
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                self.cursor.execute(sql_position)
                self.connection.commit()
                show_successful_message(self, "插入成功")


                #手动发射信号
                self.data_update_signal.emit(data_list)
            except Exception as e:
                show_error_message(self, "插入错误，请检查")
                self.record_debug(e)
            self.close()


            # 单击【检查结果】按钮槽函数
    @pyqtSlot()
    def on_btn_result_clicked(self):
        exam_dialog = InsertExam(self)
        exam_dialog.setAttribute(Qt.WA_DeleteOnClose)
        # 连接槽函数
        exam_dialog.show()

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")


    def get_insert_sql_data(self) -> (str, list):

        sql = None

        #列表
        data_list = []
        #样本编号
        ID = self.__UI.lineEdit_ID.text()
        #病人编号
        patient_ID = self.__UI.lineEdit_PatientID.text()
        #样本类型
        type = self.__UI.comboBox_sample_type.currentText()
        #样本量
        sample_size = float(self.__UI.lineEdit_sample_size.text())
        #创建日期
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #修改日期
        modification_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #状态
        sample_status = "在库"

        #是否有检查结果
        result_flag = self.__UI.comboBox_result.currentText()
        box_x = self.__UI.comboBox_x.currentText()
        box_y = self.__UI.comboBox_y.currentText()
        box_loc = str(box_x)+"-"+str(box_y)
        #位置
        sample_belong = self.location

        data_list.append(ID)
        data_list.append(patient_ID)
        data_list.append(type)
        data_list.append(sample_size)
        data_list.append(creation_date)
        data_list.append(modification_date)
        data_list.append(sample_status)
        data_list.append(sample_belong)
        data_list.append(box_loc)
        data_list.append(result_flag)

        #定义sql语句
        if patient_ID != '' and ID != '' and sample_size != '':
            sql = """insert into t_sample(ID,patient_ID,type,sample_size,creation_date, modification_date,sample_status, sample_belong,box,result) 
            values('%s','%s','%s',%f,'%s','%s','%s', '%s','%s','%s')""" % (ID, patient_ID, type, sample_size, creation_date,
                                                            modification_date, sample_status, sample_belong,box_loc,result_flag)
        sql_position = """update positions set flag=1 where cubes='%s' and belong='%s' """ %(box_loc,sample_belong)
        return sql,sql_position, data_list

    # 记录debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))

