# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
#Qt相关
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal,Qt

#加载UI
from UI.Ui_AddPatient import Ui_Dialog

#导入配置文件
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import datetime


# 添加新样品类
class AddPatient(QDialog):
    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    #把当前位置location串进来了
    def __init__(self, parent=None,location=None):
        super(AddPatient, self).__init__(parent)
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
        sql,data_list = self.get_insert_sql_data()
        if sql is not None:
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                self.connection.commit()
                show_successful_message(self, "插入成功")

                #手动发射信号
                self.data_update_signal.emit(data_list)
            except Exception as e:
                show_error_message(self, "插入错误，请检查")
                self.record_debug(e)
            self.close()




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
        #病人编号
        pID = self.__UI.lineEdit_pID.text()
        #病人姓名
        pname = self.__UI.lineEdit_pname.text()
        #年龄
        age = int(self.__UI.lineEdit_age.text())
        #性别
        gender = str(self.__UI.comboBox_gender.currentText())
        #联系电话
        phone = self.__UI.lineEdit_phone.text()
        #是否有诊断结果
        result_flag = self.__UI.comboBox_result.currentText()
        # 创建日期
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        data_list.append(pID)
        data_list.append(pname)
        data_list.append(age)
        data_list.append(gender)
        data_list.append(phone)
        data_list.append(result_flag)
        data_list.append(creation_date)

        sql = """insert into patients(patient_ID, patient_name, age, gender,phone, result, create_date) 
            values('%s','%s','%d','%s','%s','%s','%s')""" % (pID,pname,age,gender,phone, result_flag,creation_date)

        print(sql)
        return sql, data_list

    # 记录debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))

