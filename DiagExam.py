# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
import numpy as np

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
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class DiagExam(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(DiagExam, self).__init__(parent)
        # 为查询进行配置
        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]
        self.dict = {"APTT":0,"Ag":1,"全血凝固时间":2,"血浆蛋白":3,"凝血因子活性":4,"结合胆红素":5,"PP":6,"血糖":7}
        self.age_list = []
        self.gender_list = []

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()



        # 初始化ui
        self.initUI()




    def initUI(self):
        self.setWindowTitle("按病人分析诊断结果")
        self.setMinimumSize(1200, 800)

        self.cb = QComboBox()
        self.cb.addItems(["按照VWD亚型分析","按照血友病类型分析", "按照出血/血栓分析"])
        self.btn = QPushButton("确定", self)  # 确定按钮

        self.btn.clicked.connect(self.cao)  # 绑定槽函数，确定后，显示后续所有ui

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.cb)
        hlayout.addWidget(self.btn)

        hwidget = QWidget(self)
        hwidget.setLayout(hlayout)

        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.setVisible(False)
        self.myHtml.move(10, 50)
        self.myHtml.resize(1000, 600)




    def cao(self):
        self.myHtml.setVisible(True)
        if self.cb.currentText() == '按照VWD亚型分析':
            self.vwd_chart()
        else:
            pass

    def vwd_chart(self):
        tab = Tab()
        tab.add(self.vwd_blood_bar("血型分析"), "血型")
        tab.add(self.vwd_aptt_boxplot("APTT分析"), "APTT")
        tab.add(self.vwd_ag_boxplot("Ag分析"), "Ag")
        tab.add(self.vwd_act_boxplot("Act分析"), "Act")
        # tab.add(self.vwd_ripa_boxplot("RIPA分析"), "RIPA")

        tab.render("vwd_exam_tab.html")
        self.load_url("vwd_exam_tab.html")

    def vwd_blood_bar(self,title):
        x_data = ['1','2A','2B','2M','2N','3']
        a = []
        b = []
        o = []
        ab = []
        for x in x_data:
            sql_a = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='A' AND Diagnosis_table.vwd_type='%s'""" % (x)
            sql_b = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='B' AND Diagnosis_table.vwd_type='%s'""" % (x)
            sql_o = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='O' AND Diagnosis_table.vwd_type='%s'""" % (x)
            sql_ab = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='AB' AND Diagnosis_table.vwd_type='%s'""" % (x)


            self.cursor.execute(sql_a)
            a_num = self.cursor.fetchone()[0]

            self.cursor.execute(sql_b)
            b_num = self.cursor.fetchone()[0]

            self.cursor.execute(sql_o)
            o_num = self.cursor.fetchone()[0]

            self.cursor.execute(sql_ab)
            ab_num = self.cursor.fetchone()[0]


            a_ration = a_num / (a_num + b_num+o_num+ab_num)
            b_ration = b_num / (a_num + b_num+o_num+ab_num)
            o_ration = o_num / (a_num + b_num+o_num+ab_num)
            ab_ration = ab_num / (a_num + b_num+o_num+ab_num)

            a.append(a_ration)
            b.append(b_ration)
            o.append(o_ration)
            ab.append(ab_ration)


        c = (
            Bar()
                .add_xaxis(x_data)
                .add_yaxis("A", a, stack="stack1")
                .add_yaxis("B", b, stack="stack1")
                .add_yaxis("O", o, stack="stack1")
                .add_yaxis("AB", ab, stack="stack1")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="性别比例"))
        )
        return c

    def vwd_aptt_boxplot(self,title):
        vwd_type = ['1', '2A', '2B', '2M', '2N', '3']
        aptt_list = []
        for x in vwd_type:
            sql = """SELECT Exam_table.APTT FROM Diagnosis_table INNER JOIN Exam_table ON Exam_table.patient_ID = Diagnosis_table.patient_ID
                        WHERE Diagnosis_table.vwd_type='%s' AND Exam_table.APTT is not null""" %(x)

            self.cursor.execute(sql)
            aptt = [i[0] for i in self.cursor.fetchall()]
            aptt_list.append((aptt))

        c = Boxplot()
        c.add_xaxis([title])

        c.add_yaxis("1型", c.prepare_data([aptt_list[0]]))
        c.add_yaxis("2A", c.prepare_data([aptt_list[1]]))
        c.add_yaxis("2B", c.prepare_data([aptt_list[2]]))
        c.add_yaxis("2M", c.prepare_data([aptt_list[3]]))
        c.add_yaxis("2N", c.prepare_data([aptt_list[4]]))
        c.add_yaxis("3型", c.prepare_data([aptt_list[5]]))

        c.set_global_opts(title_opts=opts.TitleOpts(title="APTT统计"))
        return c

    def vwd_ag_boxplot(self,title):
        vwd_type = ['1', '2A', '2B', '2M', '2N', '3']
        ag_list = []
        for x in vwd_type:
            sql = """SELECT Exam_table.Ag FROM Diagnosis_table INNER JOIN Exam_table ON Exam_table.patient_ID = Diagnosis_table.patient_ID
                        WHERE Diagnosis_table.vwd_type='%s' AND Exam_table.Ag is not null""" %(x)

            self.cursor.execute(sql)
            ag = [i[0] for i in self.cursor.fetchall()]
            ag_list.append((ag))

        c = Boxplot()
        c.add_xaxis([title])

        c.add_yaxis("1型", c.prepare_data([ag_list[0]]))
        c.add_yaxis("2A", c.prepare_data([ag_list[1]]))
        c.add_yaxis("2B", c.prepare_data([ag_list[2]]))
        c.add_yaxis("2M", c.prepare_data([ag_list[3]]))
        c.add_yaxis("2N", c.prepare_data([ag_list[4]]))
        c.add_yaxis("3型", c.prepare_data([ag_list[5]]))

        c.set_global_opts(title_opts=opts.TitleOpts(title="Ag统计"))
        return c

    def vwd_act_boxplot(self, title):
        vwd_type = ['1', '2A', '2B', '2M', '2N', '3']
        act_list = []
        for x in vwd_type:
            sql = """SELECT Exam_table.Act FROM Diagnosis_table INNER JOIN Exam_table ON Exam_table.patient_ID = Diagnosis_table.patient_ID
                          WHERE Diagnosis_table.vwd_type='%s' AND Exam_table.Act is not null""" % (x)

            self.cursor.execute(sql)
            act = [i[0] for i in self.cursor.fetchall()]
            act_list.append((act))

        c = Boxplot()
        c.add_xaxis([title])

        c.add_yaxis("1型", c.prepare_data([act_list[0]]))
        c.add_yaxis("2A", c.prepare_data([act_list[1]]))
        c.add_yaxis("2B", c.prepare_data([act_list[2]]))
        c.add_yaxis("2M", c.prepare_data([act_list[3]]))
        c.add_yaxis("2N", c.prepare_data([act_list[4]]))
        c.add_yaxis("3型", c.prepare_data([act_list[5]]))

        c.set_global_opts(title_opts=opts.TitleOpts(title="Act统计"))
        return c





    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)






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
