# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

#作图相关
import pyecharts.options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Boxplot
from pyecharts.components import Table
from pyecharts.charts import Bar,Pie
from pyecharts.charts import Tab

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure





# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ExamStatis(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(ExamStatis, self).__init__(parent)
        # 为查询进行配置
        self.histdata = []
        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]
        self.dict = {"APTT":0,"Ag":1,"全血凝固时间":2,"血浆蛋白":3,"凝血因子活性":4,"结合胆红素":5,"PP":6,"血糖":7}

        self.age_list = []
        self.gender_list = []

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()
        #先抓取所有的数据
        self.generate_data()
        # 初始化ui
        self.initUI()

    def generate_data(self):
        #总体情况
        sql_aptt = """SELECT APTT FROM Exam_table WHERE APTT IS NOT NULL"""
        self.cursor.execute(sql_aptt)
        aptt_tuple = list(self.cursor.fetchall())
        aptt_list = [i[0] for i in aptt_tuple]

        sql_ag = """SELECT Ag FROM Exam_table WHERE Ag IS NOT NULL"""
        self.cursor.execute(sql_ag)
        ag_tuple = self.cursor.fetchall()
        ag_list = [i[0] for i in ag_tuple]

        sql_act = """SELECT Act FROM Exam_table WHERE Act IS NOT NULL"""
        self.cursor.execute(sql_act)
        act_tuple = self.cursor.fetchall()
        act_list = [i[0] for i in act_tuple]

        sql_ripa = """SELECT RIPA FROM Exam_table WHERE RIPA IS NOT NULL"""
        self.cursor.execute(sql_ripa)
        ripa_tuple = self.cursor.fetchall()
        ripa_list = [i[0] for i in ripa_tuple]

        sql_fv3c = """SELECT FV3C FROM Exam_table WHERE FV3C IS NOT NULL"""
        self.cursor.execute(sql_fv3c)
        fv3c_tuple = self.cursor.fetchall()
        fv3c_list = [i[0] for i in fv3c_tuple]

        sql_fv3c = """SELECT FV3C FROM Exam_table WHERE FV3C IS NOT NULL"""
        self.cursor.execute(sql_fv3c)
        fv3c_tuple = self.cursor.fetchall()
        fv3c_list = [i[0] for i in fv3c_tuple]

        sql_cb = """SELECT CB FROM Exam_table WHERE CB IS NOT NULL"""
        self.cursor.execute(sql_cb)
        cb_tuple = self.cursor.fetchall()
        cb_list = [i[0] for i in cb_tuple]

        sql_pp = """SELECT pp FROM Exam_table WHERE pp IS NOT NULL"""
        self.cursor.execute(sql_pp)
        pp_tuple = self.cursor.fetchall()
        pp_list = [i[0] for i in pp_tuple]

        sql_bs = """SELECT BS FROM Exam_table WHERE BS IS NOT NULL"""
        self.cursor.execute(sql_bs)
        bs_tuple = self.cursor.fetchall()
        bs_list = [i[0] for i in bs_tuple]

        self.db_list = [aptt_list, ag_list, act_list, ripa_list, fv3c_list, cb_list, pp_list, bs_list]


        #按性别
        sql_aptt_f = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
WHERE Patient_table.gender='女' and Exam_table.APTT is not null"""
        self.cursor.execute(sql_aptt_f)
        aptt_f_tuple = list(self.cursor.fetchall())
        aptt_f_list = [i[0] for i in aptt_f_tuple]

        sql_aptt_m = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
        WHERE Patient_table.gender='男' and Exam_table.APTT is not null """
        self.cursor.execute(sql_aptt_m)
        aptt_m_tuple = list(self.cursor.fetchall())
        aptt_m_list = [i[0] for i in aptt_m_tuple]

        aptt_gender = {'女':aptt_f_list,'男':aptt_m_list}

        sql_ag_f = """SELECT Exam_table.Ag FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
        WHERE Patient_table.gender='女' and Exam_table.Ag is not null"""
        self.cursor.execute(sql_ag_f)
        ag_f_tuple = list(self.cursor.fetchall())
        ag_f_list = [i[0] for i in ag_f_tuple]
        sql_ag_m = """SELECT Exam_table.Ag FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                WHERE Patient_table.gender='男'and Exam_table.Ag is not null """
        self.cursor.execute(sql_ag_m)
        ag_m_tuple = list(self.cursor.fetchall())
        ag_m_list = [i[0] for i in ag_m_tuple]
        ag_gender = {'女': ag_f_list,'男': ag_m_list}

        self.gender_list=[aptt_gender,ag_gender]

        #按年龄
        sql_aptt1 = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
        WHERE Patient_table.Age<18 and Exam_table.APTT is not null"""
        self.cursor.execute(sql_aptt1)
        aptt1_tuple = list(self.cursor.fetchall())
        aptt1_list = [i[0] for i in aptt1_tuple]

        sql_aptt2 = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                WHERE Patient_table.Age>18 and  Patient_table.Age<=35 and Exam_table.APTT is not null"""
        self.cursor.execute(sql_aptt2)
        aptt2_tuple = list(self.cursor.fetchall())
        aptt2_list = [i[0] for i in aptt2_tuple]

        sql_aptt3 = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                        WHERE Patient_table.Age>35 and  Patient_table.Age<=60 and Exam_table.APTT is not null"""
        self.cursor.execute(sql_aptt3)
        aptt3_tuple = list(self.cursor.fetchall())
        aptt3_list = [i[0] for i in aptt3_tuple]

        sql_aptt4 = """SELECT Exam_table.APTT FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                                WHERE Patient_table.Age>60 and Exam_table.APTT is not null"""
        self.cursor.execute(sql_aptt4)
        aptt4_tuple = list(self.cursor.fetchall())
        aptt4_list = [i[0] for i in aptt4_tuple]

        aptt_age = {'18以下': aptt1_list, '18-35': aptt2_list,'35-60':aptt3_list,"60以上":aptt4_list}
        self.age_list = [aptt_age]



    def initUI(self):
        data = [36.2, 46.0, 70.0, 57.7, 34.7, 40.5, 30.2, 46.6, 40.8, 37.4, 28.1, 31.8, 41.9, 29.3, 33.3, 47.7, 40.9,
                37.4, 36.0, 66.0, 47.1, 40.4, 31.9, 31.1, 96.5, 32.2, 28.8, 36.3, 34.7, 63.7, 36.2, 102.5, 102.5, 35.5,
                35.5, 33.8, 33.8, 32.4, 41.6, 37.8, 31.3, 36.6, 36.6, 56.9, 56.9, 36.2, 32.9, 41.9, 47.5, 63.0, 63.0,
                48.0, 48.0, 45.6, 45.6, 49.7, 45.2, 45.2, 42.5, 42.5, 41.0, 41.0, 51.3, 47.6, 47.6, 40.4, 40.2, 44.1,
                44.1, 66.7, 66.7, 62.0, 62.0, 58.0, 58.0, 55.2, 55.2, 65.1, 72.0, 72.0, 54.6, 64.6, 57.4, 71.0, 57.0,
                57.0, 67.7, 64.5, 60.8, 68.6, 82.8, 82.8, 79.7, 54.3, 54.3, 63.6, 63.6, 80.9, 80.9, 58.2, 58.2, 65.4,
                52.2, 52.2, 78.3, 78.3, 64.7, 62.5, 62.5, 58.2, 58.2, 54.7, 54.7, 58.1, 58.1, 56.2, 56.2, 70.9, 70.9,
                45.3, 45.3, 48.0, 42.0, 37.0, 49.4, 47.0, 41.1, 41.1, 43.1, 42.5, 43.0, 42.7, 47.9, 50.0, 50.0, 36.0,
                42.3, 44.0, 51.5, 31.7, 53.0, 40.3, 37.2, 37.2, 37.2, 37.2, 44.3, 45.4, 45.4, 43.2, 43.2, 40.5, 55.0,
                36.8, 47.0, 49.0, 49.4, 36.8, 36.1, 36.1, 36.1, 36.1, 35.9, 38.4, 38.5, 40.7, 31.5, 31.5, 39.2, 34.0,
                34.0, 47.3, 42.2, 43.5, 37.6, 37.4, 35.3, 35.3, 35.6, 39.0, 45.7, 110.0, 110.0, 62.9, 62.9, 63.2, 63.2,
                61.8, 60.2, 60.2, 37.2, 37.0]



        self.sc = MplCanvas(self, width=10, height=6, dpi=100)

        num_bins = 40
        n, bins, patches = self.sc.axes.hist(data, num_bins,
                                        density=1,
                                        alpha=0.7)

        # 工具栏
        toolbar = NavigationToolbar(self.sc, self)

        self.cmb = QComboBox(self)
        self.cmb.addItems(["整体","血型","APTT", "Ag", "全血凝固时间","血浆蛋白","凝血因子活性","结合胆红素","PP","血糖"])

        btn = QPushButton("确定", self)  # 确定按钮
        btn.clicked.connect(self.cao)  # 绑定槽函数，确定后，显示后续所有ui

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.cmb)
        hlayout.addWidget(btn)
        hweidgt = QtWidgets.QWidget(self)
        hweidgt.setLayout(hlayout)


        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(hweidgt)
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget(self)
        widget.setLayout(layout)

        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)




    def cao(self):
        if self.cmb.currentText() == '整体':
            self.new_diag = QDialog(self)
            self.new_diag.setAttribute(Qt.WA_DeleteOnClose)
            self.new_diag.resize(1000,600)
            self.new_diag.show()

            self.myHtml = QWebEngineView(self.new_diag)  # 浏览器引擎控件
            self.myHtml.resize(1000, 600)
            self.myHtml.show()

            #做图部分
            table = Table()
            headers = ["统计项", "APTT", "Ag", "全血凝固时间", "血浆蛋白", "凝血因子活性", "结合胆红素", "PP", "血糖"]

            count_list = []
            mean_list = []
            var_list = []
            sd_list = []
            max_list = []
            up_list = []
            median_list = []
            down_list = []
            min_list = []
            for dt in self.db_list:
                count_list.append(len(dt))
                mean_list.append(np.round(np.mean(dt), 2))
                var_list.append(np.round(np.var(dt), 2))
                sd_list.append(np.round(np.std(dt), 2))
                max_list.append(max(dt))
                up_list.append(np.round(np.percentile(dt, 75), 2))
                median_list.append(np.round(np.median(dt), 2))
                down_list.append(np.round(np.percentile(dt, 25), 2))
                min_list.append(min(dt))

            rows = [
                ["数量", count_list[0], count_list[1], count_list[2], count_list[3], count_list[4], count_list[5],
                 count_list[6], count_list[7]],
                ["平均值", mean_list[0], mean_list[1], mean_list[2], mean_list[3], mean_list[4], mean_list[5],
                 mean_list[6], mean_list[7]],
                ["方差", var_list[0], var_list[1], var_list[2], var_list[3], var_list[4], var_list[5], var_list[6],
                 var_list[7]],
                ["标准差", sd_list[0], sd_list[1], sd_list[2], sd_list[3], sd_list[4], sd_list[5], sd_list[6], sd_list[7]],
                ["max", max_list[0], max_list[1], max_list[2], max_list[3], max_list[4], max_list[5], max_list[6],
                 max_list[7]],
                ["75%", up_list[0], up_list[1], up_list[2], up_list[3], up_list[4], up_list[5], up_list[6], up_list[7]],
                ["50%", median_list[0], median_list[1], median_list[2], median_list[3], median_list[4], median_list[5],
                 median_list[6], median_list[7]],
                ["25%", down_list[0], down_list[1], down_list[2], down_list[3], down_list[4], down_list[5],
                 down_list[6], down_list[7]],
                ["min", min_list[0], min_list[1], min_list[2], min_list[3], min_list[4], min_list[5], min_list[6],
                 min_list[7]]
            ]
            table.add(headers, rows)
            table.set_global_opts(
                title_opts=ComponentTitleOpts(title="Table")
            )
            table.render("table_base.html")
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"table_base.html"))
            local_url = QUrl.fromLocalFile(file_path)
            print(local_url)
            self.myHtml.load(local_url)



        elif self.cmb.currentText() == '血型':
            blood_type = ['A', 'B', 'O', 'AB']
            blood_num = []
            for blood in blood_type:
                sql = """select count(1) from Exam_table where blood_type='%s'""" % (blood)
                self.cursor.execute(sql)
                blood_num.append(self.cursor.fetchone()[0])


            self.sc.axes.cla()

            self.sc.axes.pie(blood_num,
                    labels=blood_type,  # 设置饼图标签
                    colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
                    )

            self.sc.draw()

        else:
            project = self.cmb.currentText()
            self.histdata = self.db_list[self.dict[project]]
            self.sc.axes.cla()

            num_bins = 40
            n, bins, patches = self.sc.axes.hist(self.histdata, num_bins,
                                                 density=1,
                                                 alpha=0.7)
            self.sc.draw()


    def load_url(self,object,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        object.load(local_url)






##  ============================== 功能函数区 ==============================#

    # 设置cursor和connection

    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    # 记录Debug信息

    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
