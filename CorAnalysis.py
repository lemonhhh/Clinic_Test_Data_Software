# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import numpy as np
import random
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

from UI.Ui_TestWindow import Ui_Dialog
from  UI.Ui_pvalueWindow import Ui_p_diag
from UI.Ui_CorWindow import Ui_Dialog
import scipy.stats as stats
from scipy.stats import pearsonr,spearmanr,kendalltau


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message

from pyecharts import options as opts
from pyecharts.charts import HeatMap
from pyecharts.faker import Faker

class PDialog(QDialog):
    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(PDialog, self).__init__(parent)
        #设置ui
        self.__UI = Ui_p_diag()
        self.__UI.setupUi(self)


class CorExam(QDialog):
    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(CorExam, self).__init__(parent)
        self.index1 = None
        self.index2 = None

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
    def on_btn_confirm_clicked(self):
        self.index1 = self.__UI.cb1.currentText()
        self.index2 = self.__UI.cb2.currentText()
        list1,list2 = self.generate_data(self.index1,self.index2)
        cor_value = self.compute_cor(list1,list2,self.__UI.cb_method.currentText())
        print(cor_value)
        self.__UI.lable_value.setText(str(cor_value))

        # self.new_diag = QDialog(self)
        # self.new_diag.setAttribute(Qt.WA_DeleteOnClose)
        # self.new_diag.resize(800, 800)
        # self.new_diag.show()


    def generate_data(self, column1,column2):
        #字典映射
        dict_list = {'年龄':'Age','APTT':'APTT','Ag':'Ag','Act':'Act','RIPA':'RIPA','CB':'CB','血糖':'BS',
                     '乳酸':'lactate','中性粒细胞':'neutrophiles','血红蛋白':'hemoglobin','尿素':'urea',
                     '二聚体':'dimer','血红素':'hemetocrite','舒张压':'diastolic','收缩压':'sistolic',
                     '血氧饱和度':'oxyden_saturation','血小板':'platelets'}

        project1 = dict_list[column1]
        project2 = dict_list[column2]

        if column1 == '年龄' and column2 == '年龄':
            sql = """select Age,Age from Patient_table where Age is not null"""
        if column1 == '年龄' and column2 != '年龄':
            sql = """select Age,%s from Patient_table inner join Exam_table on Patient_table.patient_ID=Exam_table.ID and Age is not null 
                and %s is not null""" % (project2,project2)

        if column1 != '年龄' and column2 == '年龄':
            sql = """select %s,Age from Patient_table inner join Exam_table on Patient_table.patient_ID=Exam_table.ID and Age is not null 
                            and %s is not null""" % (project1, project1)

        if column1 != '年龄' and column2 != '年龄':
            sql = """select %s,%s from Exam_table where %s is not null and %s is not null """ % (project1,project2,project1,project2)

        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        list1 = [i[0] for i in data]
        list2 = [i[1] for i in data]
        return list1,list2
    #
    def compute_cor(self, list1,list2,method):
        if method == 'Pearson':
            value = pearsonr(list1, list2)
        if method == 'Spearman':
            value = spearmanr(list1, list2)
        if method == 'Kendall':
            value = kendalltau(list1, list2)

        return np.round(value,2)[0]


    def get_check_list(self):
        check_list = []
        if self.__UI.cb_age.isChecked():
            check_list.append('Age')
        if self.__UI.cb_aptt.isChecked():
            check_list.append('APTT')
        if self.__UI.cb_ag.isChecked():
            check_list.append('Ag')
        if self.__UI.cb_act.isChecked():
            check_list.append('Act')
        if self.__UI.cb_ripa.isChecked():
            check_list.append('RIPA')
        if self.__UI.cb_fv3c.isChecked():
            check_list.append('FV3C')
        if self.__UI.cb_cb.isChecked():
            check_list.append('CB')
        if self.__UI.cb_pp.isChecked():
            check_list.append('pp')
        if self.__UI.cb_bs.isChecked():
            check_list.append('BS')
        if self.__UI.cb_sistolic.isChecked():
            check_list.append('sistolic')
        if self.__UI.cb_diastolic.isChecked():
            check_list.append('diastolic')
        if self.__UI.cb_lactate.isChecked():
            check_list.append('lactate')
        if self.__UI.cb_oxgen.isChecked():
            check_list.append('oxyden_saturation')
        if self.__UI.cb_plate.isChecked():
            check_list.append('platelets')
        if self.__UI.cb_urea.isChecked():
            check_list.append('urea')
        if self.__UI.cb_hemo.isChecked():
            check_list.append('hemoglobin')
        if self.__UI.cb_neu.isChecked():
            check_list.append('neutrophiles')
        if self.__UI.cb_dimer.isChecked():
            check_list.append('dimer')
        return check_list

    def generate_chart(self,columns):

        raw_data = []
        cor_values = []
        raw_data = self.generate_data(columns)

        cor_values = self.compute_cor(raw_data)

        #todo:
        value = []

        index = 0
        for i in range(len(columns)):
            for j in range(len(columns)):
                cor = cor_values[index]
                value.append([i,j,cor])
                index = index + 1


        #1:横坐标，2：纵坐标：3value
        c = (
            HeatMap()
                .add_xaxis(columns)
                .add_yaxis(
                "相关系数",
                columns,
                value,#嵌套list
                label_opts=opts.LabelOpts(is_show=True, position="inside"),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="相关系数"),
                visualmap_opts=opts.VisualMapOpts(),
            )
                .render("heatmap.html")
        )





##---------------------------------函数实现-----------------------


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
