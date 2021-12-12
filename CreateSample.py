# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from UI.Ui_CreateSampleWindow import Ui_Dialog
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import datetime


# 添加新样品类
class CreateSample(QDialog):
    #发出信号
    data_update_signal = pyqtSignal(list)

    def __init__(self, parent=None,location=None):
        super(CreateSample, self).__init__(parent)
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)

        self.connection = None
        self.cursor = None
        self.logger = None

        self.set_connection_cursor()
        self.set_logger()
        self.location = location
        print("self.location is", self.location)




    # 单击【提交】按钮槽函数
    @pyqtSlot()
    def on_btn_commit_clicked(self):

        sql, data_list = self.get_insert_sql_data()

        if sql is not None:
            try:
                self.cursor.execute(sql)  # 执行sql语句
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

    # 获取插入SQL语句
    def get_insert_sql_data(self) -> (str, list):


        sql = None
        data_list = []

        ID = self.__UI.lineEdit_ID.text()
        name = self.__UI.lineEdit_name.text()
        type = self.__UI.comboBox_sample_type.currentText()
        sample_size = float(self.__UI.lineEdit_sample_size.text())
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sample_status = "在库"
        target = "."
        print(target)

        #TO DO:需要改，怎么传过来
        #这边需要改一下
        sample_belong = self.location
        # sample_belong = "出血病冰箱-层1-架子1-抽屉5-标本盒1"
        print("sample_belong",sample_belong)

        data_list.append(ID)
        data_list.append(name)
        data_list.append(type)
        data_list.append(sample_size)
        data_list.append(creation_date)
        data_list.append(modification_date)
        data_list.append(sample_status)
        data_list.append(sample_belong)

        if name != '' and ID != '' and sample_size != '':
            sql = """insert into t_sample(ID,name,type,sample_size,creation_date, modification_date,sample_status, sample_belong) 
            values('%s','%s','%s',%f,'%s','%s','%s', '%s')""" % (ID, name, type, sample_size, creation_date,
                                                            modification_date, sample_status, sample_belong)

        return sql, data_list

    # 记录debug信息
    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))

