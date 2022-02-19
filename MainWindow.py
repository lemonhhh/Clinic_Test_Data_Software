# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QMessageBox, QTreeWidgetItem, \
    QPushButton, QComboBox, QVBoxLayout, QWidget, QFrame, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

# 导入UI
from UI.Ui_MainWindow import Ui_MainWindow
# 导入各种类【功能函数】
from CreateSample import CreateSample #添加样本
from RecycleBinDialog import RecycleBinDialog #查看回收站样本
from EnterToday import EnterToday #查看今日入库
from SearchWindow import SearchWindow #查询样本
from SampleClass import SampleClass #分析样本类别
from UseRatio import UseRatio #分析容器使用率
from InsertResult import InsertExam #插入检查结果
from SampleCalendar import SampleCalendar #按天入库样本数
from DiseaseTree import DiseaseTree #疾病树
from ExamSta import ExamStatis #检验结果统计
from AddPatient import AddPatient#添加病人
from PatientSearch import PatientSearch#查询病人信息
from PredictDisease import PredictDisease#疾病预测

# 相关配置
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
# 其他必须
import sys
import datetime
# 主题
import qdarkstyle
from qt_material import apply_stylesheet

# 主窗口
class MainWindow(QMainWindow):
    # 初始化函数
    def __init__(self):
        # 继承QMainWindow基本功能
        super(MainWindow, self).__init__()
        # self.setStyleSheet("background-color: white;") #设置背景颜色

        # 创建下拉列表
        self.frame = QFrame(self)
        self.frame.resize(823, 600)
        self.frame.setStyleSheet(
            'border-image: url("./fm.png"); background-repeat: no-repeat;')
        self.frame.move(300, 100)

        self.cb = QComboBox(self)  # 下拉列表
        self.cb.addItems(["出凝血科室", "尿液检验", "其他科室"])  # 科室名称（继续添加）
        self.cb.move(650, 750)
        self.cb.adjustSize()  # 根据长度自动调节宽度

        self.btn = QPushButton("确定", self)  # 确定按钮
        self.btn.move(750, 750)
        self.btn.clicked.connect(self.cao)  # 绑定槽函数，确定后，显示后续所有ui

    def cao(self):
        if self.cb.currentText() == '出凝血科室':
            self.__UI = Ui_MainWindow()
            self.__UI.setupUi(self)

            self.setCentralWidget(self.__UI.tabWidget)
            # self.showMaximized()
            # self.setGeometry(200, 200, 1100, 800)
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.height = self.screenRect.height()
            self.width = self.screenRect.width()
            self.setGeometry(0, 0, self.width, self.height)
            # 设置右侧tab的宽度
            self.set_tableview(
                self.__UI.tableView_show,
                horsize=130,
                versize=50)
            self.set_tableview(
                self.__UI.tableView_patient,
                horsize=130,
                versize=50)

            # 设置model
            self.data_model = self.get_model()
            self.set_model()
            # 病人信息
            self.data_model_patient = self.get_model_patient()
            self.set_model_patient()

            # 自己设置的
            self.location = ""
            # 样本id
            self.sample_id = ""
            # 病人id
            self.patiend_id = ""

            # 设置为不可见
            self.btn.setVisible(False)
            self.cb.setVisible(False)
            self.frame.setVisible(False)

            # 删除控件
            self.btn.deleteLater()
            self.cb.deleteLater()
            self.frame.deleteLater()
        # 其他科室的
        else:
            print("还没做呢")


##  ============================== 自动连接槽函数区 ==============================#
    # 点击【查询样本】
    @pyqtSlot()
    def on_search_sample_clicked(self):
        self.on_act_search_triggered()

    # 点击【新增样本】
    @pyqtSlot()
    def on_add_sample_clicked(self):
        self.on_act_create_triggered()

    # 点击【删除样本】
    @pyqtSlot()
    def on_delete_sample_clicked(self):
        self.on_act_delete_triggered()

    # 点击【查看回收站样本】
    @pyqtSlot()
    def on_trash_clicked(self):
        self.on_act_recyclebin_triggered()

    # 点击【当日入库】
    @pyqtSlot()
    def on_enter_today_clicked(self):
        self.on_act_look_today_triggered()

    # 点击【样本类别】
    @pyqtSlot()
    def on_sample_class_clicked(self):
        self.on_act_sample_class_triggered()

    # 点击【容器使用率】
    @pyqtSlot()
    def on_use_ratio_clicked(self):
        self.on_act_compute_use_triggered()

    # 点击【日期热图】
    @pyqtSlot()
    def on_calendar_clicked(self):
        self.on_act_calendar_triggered()

    # 点击【添加检验结果】
    @pyqtSlot()
    def on_add_exam_clicked(self):
        self.on_act_addexam_triggered()

    #点击【添加病人】
    @pyqtSlot()
    def on_add_patient_clicked(self):
        print("添加病人")
        # 示例化样本
        add_patient_dialog = AddPatient(self)
        add_patient_dialog.setAttribute(Qt.WA_DeleteOnClose)
        # 连接槽函数
        add_patient_dialog.data_update_signal.connect(self.do_receive_data)
        add_patient_dialog.show()


    # 点击【病人信息】
    @pyqtSlot()
    def on_patient_info_clicked(self):
        print("病人信息查询")
        psearch_dialog = PatientSearch(self)
        psearch_dialog.setAttribute(Qt.WA_DeleteOnClose)
        psearch_dialog.show()

    #点击【添加病史】
    @pyqtSlot()
    def on_add_history_clicked(self):
        print("添加病史")
        # psearch_dialog = PatientSearch(self)
        # psearch_dialog.setAttribute(Qt.WA_DeleteOnClose)
        # psearch_dialog.show()

    @pyqtSlot()
    def on_predict_disease_clicked(self):
        print("疾病预测")
        predict_dialog = PredictDisease(self)
        predict_dialog.setAttribute(Qt.WA_DeleteOnClose)
        predict_dialog.show()

    # 疾病介绍
    @pyqtSlot()
    def on_disease_tree_clicked(self):
        disease_widget = DiseaseTree(self)
        # sample_class_widget.setAttribute(Qt.WA_DeleteOnClose)
        disease_widget.show()

    # 检验数据统计
    @pyqtSlot()
    def on_exam_sta_clicked(self):
        exam_sta_widget = ExamStatis(self)
        exam_sta_widget.setAttribute(Qt.WA_DeleteOnClose)
        exam_sta_widget.show()

    # 检验数据统计
    # todo:
    # 可以设置一些简单的规则
    @pyqtSlot()
    def on_auto_diag_clicked(self):
        print("自动诊断")
        try:   # 执行sql语句
            sql1 = """UPDATE diagnosis INNER JOIN exam_result ON diagnosis.patient_ID=exam_result.patient_ID SET diagnosis.auto_result = '出血病' WHERE (exam_result.pt >= 17 OR exam_result.aptt >= 38) """
            sql2 = """UPDATE diagnosis INNER JOIN exam_result ON diagnosis.patient_ID=exam_result.patient_ID SET diagnosis.auto_result = '血栓病' WHERE (exam_result.pt <= 8 OR exam_result.aptt <= 15) """


            connection_auto = get_sql_connection()
            cursor_auto = connection_auto.cursor()
            cursor_auto.execute(sql1)
            cursor_auto.execute(sql2)
            connection_auto.commit()
            show_successful_message(self, "自动标注成功")

        except Exception as e:
            print(e)
            show_error_message(self, "删除错误，请检查")

    # 槽函数(为了删除样本)

    def talbe_choose(self):
        row = (self.__UI.tableView_show.currentIndex().row())
        id_data = (self.data_model.itemData(self.data_model.index(row, 0)))
        p_data = (self.data_model.itemData(self.data_model.index(row, 1)))
        self.sample_id = (id_data[0])
        self.patiend_id = (p_data[0])

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    # 目录树节点变化
    def on_treeWidget_show_currentItemChanged(
            self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        flg = False
        # 表示已经到最后一级了
        if current.childCount() == 0:
            flg = True

        # 是当前选中的widget
        first_name = current.text(0)

        # 递归地找到路径
        while current.parent() is not None:
            current = current.parent()
            first_name = current.text(0) + '-' + first_name

        self.data_model = self.get_raw_model(
            labels=[
                '样本编号',
                '病人编号',
                '样本类型',
                '样本量',
                '添加日期',
                '更新时间',
                '状态',
                '归属',
                '位置',
                '是否有检查结果'],
            colCount=10)
        # 连接到数据库
        connection = get_sql_connection()
        # 创建游标
        cursor = connection.cursor()

        # 已经到最后一级
        if flg:
            sql = """select * from t_sample where t_sample.sample_belong = '%s' """ % first_name
        else:
            sql = """select * from t_sample where t_sample.sample_belong like '""" + \
                first_name + """%'"""
        # 执行查询结果
        cursor.execute(sql)

        if self.__UI.tableView_show.model() is not None:
            self.__UI.tableView_show.model().clear()

        if cursor.rowcount != 0:
            self.data_model = self.add_model_data(
                self.data_model, list(cursor.fetchall()))
            self.set_model()
        # 传入的参数
        self.location = first_name

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    # 目录树节点变化
    def on_treeWidget_patient_currentItemChanged(
            self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        flg = False
        # 表示已经到最后一级了
        if current.childCount() == 0:
            flg = True

        # 是当前选中的widget
        first_name = []
        first_name.append(current.text(0))

        # 递归地找到路径
        while current.parent() is not None:
            current = current.parent()
            first_name.append(current.text(0))

        self.data_model_patient = self.get_raw_model(
            labels=[
                '病人编号',
                '病人姓名',
                '年龄',
                '联系方式',
                '性别',
                '诊断结果',
                '添加日期'],
            colCount=7)
        # 连接到数据库
        connection = get_sql_connection()
        # 创建游标
        cursor = connection.cursor()
        # 已经到最后一级

        if flg:
            types = first_name[0]
            if types == '女性':
                target = '女'
                sql = """select * from patients where gender = '%s' """ % target
            if types == '男性':
                target = '男'
                sql = """select * from patients where gender = '%s' """ % target
            if types == '18以下':
                target = 18
                sql = """select * from patients where age < 18 """
            if types == '18-35':
                sql = """select * from patients where age >= 18 and age <= 35 """
            if types == '36-60':
                sql = """select * from patients where age >= 36 and age <= 60 """
            if types == '60以上':
                sql = """select * from patients where age >60"""

        else:
            sql = """select * from patients"""

        # 执行查询结果
        cursor.execute(sql)

        if self.__UI.tableView_patient.model() is not None:
            self.__UI.tableView_patient.model().clear()

        if cursor.rowcount != 0:
            self.data_model_patient = self.add_model_data(
                self.data_model_patient, list(cursor.fetchall()))

            self.set_model_patient()
##  ============================== 槽函数区 ==============================#

    # 点击【新增】选项槽函数

    @pyqtSlot()
    def on_act_create_triggered(self):
        # 示例化样本
        creation_dialog = CreateSample(self, self.location)
        creation_dialog.setAttribute(Qt.WA_DeleteOnClose)
        # 连接槽函数
        creation_dialog.data_update_signal.connect(self.do_receive_data)
        creation_dialog.show()

    # 点击【查询】槽函数
    @pyqtSlot()
    def on_act_search_triggered(self):
        search_dialog = SearchWindow(self)
        search_dialog.setAttribute(Qt.WA_DeleteOnClose)
        search_dialog.show()

    # 点击【添加结果】槽函数
    @pyqtSlot()
    def on_act_addexam_triggered(self):
        add_dialog = InsertExam(self, self.sample_id, self.patiend_id)  # 示例化
        add_dialog.setAttribute(Qt.WA_DeleteOnClose)
        add_dialog.show()

    # 点击【删除】槽函数
    def on_act_delete_triggered(self):
        try:
            sample_id = str(self.sample_id)

            sql_find = """select * from t_sample where ID='%s' """ % (sample_id)

            connection_find = get_sql_connection()  # 建立链接
            cursor_find = connection_find.cursor()  # 建立游标
            cursor_find.execute(sql_find)  # 执行查询
            data_find = cursor_find.fetchone()
            print(data_find)

            # 得到数据
            ID = data_find[0]
            patient_id = data_find[1]
            type = data_find[2]
            sample_size = data_find[3]
            creation_date = data_find[4]
            modification_date = data_find[5]
            sample_status = '回收站'
            sample_belong = data_find[7]
            box_loc = data_find[8]

            # 插入到回收站数据库中
            sql_insert = """insert into recycle_sample(ID,patinent_ID,type,sample_size,creation_date, modification_date,sample_status, sample_belong,box)
                values('%s','%s','%s',%f,'%s','%s','%s', '%s','%s')""" % (ID, patient_id, type, sample_size, creation_date,
                                                                          modification_date, sample_status, sample_belong, box_loc)
            # 删除
            sql = """delete from t_sample where ID='%s' """ % (sample_id)


            connection_insert = get_sql_connection()
            cursor_insert = connection_insert.cursor()
            cursor_insert.execute(sql_insert)
            connection_insert.commit()

            connection_delete = get_sql_connection()
            cursor_delete = connection_delete.cursor()
            cursor_delete.execute(sql)
            connection_delete.commit()

            show_successful_message(self, "删除成功")

        except Exception as e:
            show_error_message(self, "删除错误，请检查")

    # 点击【回收站】槽函数
    @pyqtSlot()
    def on_act_recyclebin_triggered(self):
        recycle_dialog = RecycleBinDialog(self)
        recycle_dialog.setAttribute(Qt.WA_DeleteOnClose)
        recycle_dialog.show()

    # 点击【今日入库】槽函数
    def on_act_look_today_triggered(self):
        today_dialog = EnterToday(self)
        today_dialog.setAttribute(Qt.WA_DeleteOnClose)
        today_dialog.show()

    # 点击【样本类别】槽函数
    def on_act_sample_class_triggered(self):
        sample_class_widget = SampleClass(self)
        # sample_class_widget.setAttribute(Qt.WA_DeleteOnClose)
        sample_class_widget.show()

    # 点击【样本类别】槽函数

    @pyqtSlot()
    def on_act_compute_use_triggered(self):
        ratio_dialog = UseRatio(self)
        ratio_dialog.setAttribute(Qt.WA_DeleteOnClose)
        ratio_dialog.show()

        # 点击【样本类别】槽函数
    @pyqtSlot()
    def on_act_calendar_triggered(self):
        calender_dialog = SampleCalendar(self)
        calender_dialog.setAttribute(Qt.WA_DeleteOnClose)
        calender_dialog.show()
##  ===========================================================================#

##  ============================== 自定义槽函数区 ==============================#

    @pyqtSlot(list)
    def do_receive_data(self, data_list: list):
        self.data_model = self.add_model_data(self.data_model, data_list)

##  ===========================================================================#

    # 获取数据模型
    def get_model(self):
        raw_model = self.get_raw_model(
            labels=[
                '样本编号',
                '病人编号',
                '样本类型',
                '样本量',
                '添加日期',
                '更新时间',
                '状态',
                '归属',
                '位置',
                '是否有检查结果'],
            colCount=10)
        # 从数据库中得到所有的数据
        data_list = self.read_sql_data()

        if len(data_list) > 0:
            return self.add_model_data(raw_model, data_list)

    # todo:
    # 先去改add_model_data了
    def get_model_patient(self):
        raw_model = self.get_raw_model(
            labels=[
                '病人编号',
                '病人姓名',
                '年龄',
                '联系方式',
                '性别',
                '诊断结果',
                '添加日期'],
            colCount=7)
        # 从数据库中得到所有的数据
        data_list = self.read_sql_data_patient()

        if len(data_list) > 0:
            return self.add_model_data(raw_model, data_list)

    # 获取无数据的数据模型
    def get_raw_model(
            self,
            labels: list,
            colCount: int = 2) -> QStandardItemModel:
        '''
        获取无数据的数据模型
        :param colCount:要设置的列数
        :return:无数据的数据模型
        '''
        raw_model = QStandardItemModel(0, colCount)
        raw_model.setHorizontalHeaderLabels(labels)
        return raw_model

    # 读取数据库数据
    def read_sql_data(self) -> list:
        # 获取数据库的连接
        connection = get_sql_connection()
        # 建立游标
        cursor = connection.cursor()
        # 执行sql语句
        cursor.execute('select * from t_sample;')
        # 返回全部内容
        return cursor.fetchall()

    # 读病人数据库
    def read_sql_data_patient(self) -> list:
        # 获取数据库的连接
        connection = get_sql_connection()
        # 建立游标
        cursor = connection.cursor()
        # 执行sql语句
        cursor.execute('select * from patients;')
        # 返回全部内容
        return cursor.fetchall()

    # 向模型添加数据

    def add_model_data(self, model: QStandardItemModel,
                       data_list: list) -> QStandardItemModel:
        fun = self.choose_add_function(data_list)
        if fun is None:
            show_error_message(self, "数据类型错误,请检查")
            return

        final_model = fun(model, data_list)

        return final_model

    # 生产者函数：选择添加模式
    def choose_add_function(self, data_list: list):
        method = None
        if isinstance(data_list[0], tuple):
            method = self.add_multiple_data
        else:
            method = self.add_single_data

        return method

    # 添加单条记录
    def add_single_data(self, model: QStandardItemModel,
                        record: list) -> QStandardItemModel:
        return model.appendRow(
            [QStandardItem(self.process_data(item)) for item in record])

    # 添加多条信息
    def add_multiple_data(
            self,
            model: QStandardItemModel,
            data_list: list) -> QStandardItemModel:
        for record in data_list:
            row = []
            for item in record:
                item = self.process_data(item)
                row.append(QStandardItem(item))

            model.appendRow(row)

        return model

    # 处理数据
    def process_data(self, data: any) -> any:
        if isinstance(data, str):
            pass
        elif isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data = str(data)

        return data

    # 初始化table_view函数
    def set_tableview(
            self,
            widget: QTableView,
            horsize: int,
            versize: int,
            is_altercolor=True) -> None:
        widget.setAlternatingRowColors(is_altercolor)
        widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        widget.setSelectionMode(QAbstractItemView.SingleSelection)
        widget.horizontalHeader().setDefaultSectionSize(horsize)
        widget.verticalHeader().setDefaultSectionSize(versize)
        widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 设置数据模型
    def set_model(self):
        if self.data_model is None:
            return
        self.__UI.tableView_show.setModel(self.data_model)

    def set_model_patient(self):
        if self.data_model_patient is None:
            return
        self.__UI.tableView_patient.setModel(self.data_model_patient)
##  =======================================================================#


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # 设置app主题
    # apply_stylesheet(app, theme='light_cyan_500.xml')
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    win.showFullScreen()
    win.show()
    sys.exit(app.exec())
