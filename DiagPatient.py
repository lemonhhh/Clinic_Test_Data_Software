# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import json
import numpy as np

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox, QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

# 作图相关
import pyecharts.options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Boxplot
from pyecharts.components import Table
from pyecharts.charts import Bar, Pie
from pyecharts.charts import Tab
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class DiagPatient(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(DiagPatient, self).__init__(parent)
        # 为查询进行配置
        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]
        self.dict = {
            "APTT": 0,
            "Ag": 1,
            "全血凝固时间": 2,
            "血浆蛋白": 3,
            "凝血因子活性": 4,
            "结合胆红素": 5,
            "PP": 6,
            "血糖": 7}

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
        self.cb.addItems(["按照VWD亚型分析", "按照血友病类型分析", "按照出血/血栓分析"])
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
            x_data = ['1', '2A', '2B', '2M', '2N', '3']
            column = 'vwd_type'
        elif self.cb.currentText() == '按照血友病分析':
            x_data = ['A', 'B', 'VWD']
            column = 'haemophilia_type'
        elif self.cb.currentText() == '按照出血/血栓分析':
            x_data = ['出血病', '血栓病']
            column = 'binary_type'

        self.type_chart(x_data, column)

    def type_chart(self, x_data, column):
        tab = Tab()
        tab.add(self.type_gender_bar(x_data, column, "性别分析"), "性别")
        tab.add(self.type_age_boxplot(x_data, column, "年龄分析"), "年龄")

        tab.add(self.type_history_bar(x_data, column, "smoke", "吸烟史分析"), "吸烟史")
        tab.add(self.type_history_bar(x_data, column, "drink", "饮酒史分析"), "饮酒史")
        tab.add(self.type_history_bar(x_data,column,"transfusion","输血史分析"),"输血史")
        tab.add(self.type_history_bar(x_data,column,"operation","手术史分析"),"手术史")
        tab.add(self.type_history_bar(x_data,column,"infectious","传染史分析"),"传染史")
        tab.add(self.type_history_bar(x_data,column,"allergy","过敏史分析"),"过敏史")
        tab.render("patien_diag_tab.html")

        self.load_url("patien_diag_tab.html")

    def type_gender_bar(self, x_data, column, title):

        female = []
        male = []
        for x in x_data:
            sql_f = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                WHERE Patient_table.gender='女' AND Diagnosis_table.%s='%s'""" % (column, x)

            sql_m = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                            WHERE Patient_table.gender='男' AND Diagnosis_table.%s='%s'""" % (column, x)

            self.cursor.execute(sql_f)
            f_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_m)
            m_num = self.cursor.fetchone()[0]

            f_ration = np.round(f_num / (f_num + m_num),4)*100
            m_ration = np.round(m_num / (f_num + m_num),4)*100

            female.append(f_ration)
            male.append(m_ration)

        c = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis("女", female, stack="stack1")
            .add_yaxis("男", male, stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                             tooltip_opts=opts.TooltipOpts(formatter="{a} <br/>{b}: {c}%"))
            .set_global_opts(title_opts=opts.TitleOpts(title="性别比例"))
        )
        return c

    def type_age_boxplot(self, x_data, column, title):

        vwd_type = ['1', '2A', '2B', '2M', '2N', '3']
        age_list = []
        for x in vwd_type:
            sql = """SELECT Patient_table.Age FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                        WHERE Diagnosis_table.%s='%s' AND Patient_table.Age is not null""" % (column, x)

            self.cursor.execute(sql)
            age = [i[0] for i in self.cursor.fetchall()]
            age_list.append((age))

        c = Boxplot()
        c.add_xaxis([title])

        for i in range(len(x_data)):
            c.add_yaxis(x_data[i], c.prepare_data([age_list[i]]))

        c.set_global_opts(title_opts=opts.TitleOpts(title="年龄统计"))
        return c

    # 做图

    def type_history_bar(self, x_data, column, history, title):
        ys = []
        ns = []
        us = []
        for x in x_data:
            sql_y = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                WHERE Patient_table.%s='是' AND Diagnosis_table.vwd_type='%s'""" % (history, x)

            sql_n = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                            WHERE Patient_table.%s='否' AND Diagnosis_table.vwd_type='%s'""" % (history, x)

            sql_u = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
                                        WHERE Patient_table.%s='未知' AND Diagnosis_table.vwd_type='%s'""" % (history, x)

            self.cursor.execute(sql_y)
            y_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_n)
            n_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_u)
            u_num = self.cursor.fetchone()[0]

            y_ration = np.round(y_num / (y_num + n_num + u_num),4)*100
            n_ration = np.round(n_num / (y_num + n_num + u_num),4)*100
            u_ration = np.round(u_num / (y_num + n_num + u_num),4)*100

            ys.append(y_ration)
            ns.append(n_ration)
            us.append(u_ration)
        # todo:
        # 需要修改一下
        c = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis("是",ys,stack="stack1")
            .add_yaxis("否",ns,stack="stack1")
            .add_yaxis("未知",us,stack="stack1")
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                tooltip_opts=opts.TooltipOpts(formatter="{a} <br/>{b}: {c}%"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title)))
        return c


    def load_url(self, file_name):
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
