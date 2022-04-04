# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import numpy as np

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

from UI.Ui_TestWindow import Ui_Dialog
from  UI.Ui_pvalueWindow import Ui_p_diag

import scipy.stats as stats
# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class PDialog(QDialog):
    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(PDialog, self).__init__(parent)
        #设置ui
        self.__UI = Ui_p_diag()
        self.__UI.setupUi(self)


class TestExam(QDialog):
    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(TestExam, self).__init__(parent)
        self.p_value = None
        self.data_list = []

        self.connection = None
        self.cursor = None
        self.logger = None
        self.set_connection_cursor()
        self.set_logger()

        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)

    @pyqtSlot()
    def on_btn_help_clicked(self):
        dialog = PDialog(self)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.show()






    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.group = self.__UI.comboBox_group.currentText()
        self.project = self.__UI.comboBox_data.currentText()
        self.method = self.__UI.comboBox_method.currentText()

        #先取数据
        self.get_data(self.group,self.project,self.method)
        if self.p_value < 0.05:
            text = '<0.05'
        else:
            text = str(np.round(self.p_value,3))
        self.__UI.label_result.setText(text)


##---------------------------------函数实现-----------------------
    def get_data(self,group,project,method):
        if group == 'VWD类型':
            x_group = ['1','2A','2B','2M','2N','3']
            test_data = []
            for x in x_group:
                if(project!='年龄'):
                    sql = """SELECT Exam_table.%s FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
                     WHERE Diagnosis_table.%s='%s' and Exam_table.%s is not null""" % (project,'vwd_type',x,project)

                else:
                    sql = """SELECT Patient_table.%s FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID=Patient_table.patient_ID
                                        WHERE Diagnosis_table.%s='%s' and Patient_table.%s is not null""" % ("Age", 'vwd_type', x,"Age")

                self.cursor.execute(sql)
                data = [i[0] for i in self.cursor.fetchall()]
                test_data.append(data)

            self.data_list = test_data

            if method == 'ANOVA':
                f,self.p_value = stats.f_oneway(self.data_list[0],self.data_list[1],self.data_list[2],self.data_list[3],self.data_list[4],self.data_list[5])
                print(f,self.p_value)
            elif method == 'Kruskal-Wallis':
                s,self.p_value = stats.kruskal(self.data_list[0],self.data_list[1],self.data_list[2],self.data_list[3],self.data_list[4],self.data_list[5])
            else:
                show_error_message(self, "请选择正确的方法")

        elif group == '血友病类型':
            x_group = ['A','B','VWD']
            test_data = []
            for x in x_group:
                if (project != '年龄'):
                    sql = """SELECT Exam_table.%s FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
                                     WHERE Diagnosis_table.%s='%s' and Exam_table.%s is not null """ % (project, 'haemophilia_type', x,project)
                else:
                    sql = """SELECT Patient_table.%s FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID=Patient_table.patient_ID
                                                        WHERE Diagnosis_table.%s='%s' and Patient_table.%s is not null """ % ("Age", 'haemophilia_type', x,project)

                self.cursor.execute(sql)
                data = [i[0] for i in self.cursor.fetchall()]
                test_data.append(data)
            self.data_list = test_data

            if method == 'ANOVA':
                f,self.p_value = stats.f_oneway(self.data_list[0],self.data_list[1],self.data_list[2])
            elif method == 'Kruskal-Wallis':
                s,self.p_value = stats.kruskal(self.data_list[0],self.data_list[1],self.data_list[2])
            else:
                show_error_message(self, "请选择正确的方法")


        elif group == '出血/血栓':
            x_group = ['出血病','x血栓病']
            test_data = []
            for x in x_group:
                if (project != '年龄'):
                    sql = """SELECT Exam_table.%s FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
                                                 WHERE Diagnosis_table.%s='%s' and Exam_table.%s is not null """ % (project, 'binary_type', x,project)
                else:
                    sql = """SELECT Patient_table.%s FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID=Patient_table.patient_ID
                                                                    WHERE Diagnosis_table.%s='%s' and Patient_table.%s is not null""" % (
                    "Age", 'binary_type', x,"Age")

                self.cursor.execute(sql)
                data = [i[0] for i in self.cursor.fetchall()]
                test_data.append(data)
            self.data_list = test_data

            if method == 'T-test':
                f, self.p_value = stats.ttest_ind(self.data_list[0], self.data_list[1])
            elif method == 'Mann-Whitney':
                s, self.p_value = stats.kendalltau(self.data_list[0], self.data_list[1])
            else:
                show_error_message(self, "请选择正确的方法")

        elif group == '血型':
            x_group = ['A','B','AB','O']
            test_data = []
            for x in x_group:
                if (project != '年龄'):
                    sql = """SELECT Exam_table.%s FROM  Exam_table 
                                                             WHERE Exam_table.%s='%s' and Exam_table.%s is not null""" % (
                    project, 'Blood_type', x,project)
                else:
                    sql = """SELECT Patient_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID
                                                                                WHERE Exam_table.%s='%s' and Patient_table.%s is not null""" % (
                        "Age", 'Blood_type', x,"Age")

                self.cursor.execute(sql)
                data = [i[0] for i in self.cursor.fetchall()]
                test_data.append(data)
            self.data_list = test_data


            if method == 'ANOVA':
                f, self.p_value = stats.f_oneway(self.data_list[0], self.data_list[1], self.data_list[2],
                                                 self.data_list[3])
            elif method == 'Kruskal-Wallis':
                s, self.p_value = stats.kruskal(self.data_list[0], self.data_list[1], self.data_list[2],
                                                self.data_list[3])
            else:
                show_error_message(self, "请选择正确的方法")

        elif group == '性别':
            x_group = ['女','男']
            test_data = []
            for x in x_group:
                if (project != '年龄'):
                    sql = """SELECT Exam_table.%s FROM Patient_table INNER JOIN Exam_table ON Patient_table.patient_ID=Exam_table.patient_ID
                                                             WHERE Patient_table.%s='%s' and Exam_table.%s is not null""" % (
                    project, 'gender', x,project)

                else:
                    sql = """SELECT Patient_table.%s FROM Patient_table 
                                    WHERE Patient_table.%s='%s' and Patient_table.%s is not null""" % (
                        "Age", 'gender', x,"Age")

                self.cursor.execute(sql)
                data = [i[0] for i in self.cursor.fetchall()]
                test_data.append(data)
            self.data_list = test_data

            if method == 'T-test':
                f, self.p_value = stats.ttest_ind(self.data_list[0], self.data_list[1])
            elif method == 'Mann-Whitney':
                s, self.p_value = stats.kendalltau(self.data_list[0], self.data_list[1])
            else:
                show_error_message(self, "请选择正确的方法")

#--------数据库相关函数-------
    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

        # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
