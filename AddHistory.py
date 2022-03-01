# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
#Qt相关
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal,Qt

#加载UI
from UI.Ui_HistoryWindow import Ui_Dialog

#导入配置文件
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import datetime


# 添加新样品类
class AddHistory(QDialog):
    #发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    #把当前位置location串进来了
    def __init__(self, parent=None,patient_id=None):
        super(AddHistory, self).__init__(parent)
        #ui初始化
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)

        self.__UI.lineEdit_patientID.setText(patient_id)

        #初始化sql相关
        self.connection = None
        self.cursor = None
        self.logger = None

        self.set_connection_cursor()
        self.set_logger()


    # 单击【提交】按钮槽函数
    @pyqtSlot()
    def on_btn_confirm_clicked(self):
        sql,data_list = self.get_insert_sql_data()
        print("得到了sql")

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
        pID = self.__UI.lineEdit_patientID.text()

        #是否吸烟
        smoke = self.__UI.cb_smoke.currentText()
        #饮酒
        drink = self.__UI.cb_drink.currentText()
        #输血
        trans = self.__UI.cb_trans.currentText()
        #手术
        sur = self.__UI.cb_sur.currentText()
        #传染病
        infect = self.__UI.cb_infect.currentText()
        # 过敏
        allergy = self.__UI.cb_allergy.currentText()

        data_list.append(pID)
        data_list.append(smoke)
        data_list.append(drink)
        data_list.append(trans)
        data_list.append(sur)
        data_list.append(infect)
        data_list.append(allergy)

        print(data_list)

        sql = """UPDATE  history SET smoke='%s',drink='%s',transfusion='%s',operation='%s',infectious='%s',allergy='%s'
WHERE patient_ID='%s'""" % (smoke,drink,trans,sur,infect,allergy,pID)

        print("插入病史sql",sql)
        return sql, data_list

    # 记录debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))

