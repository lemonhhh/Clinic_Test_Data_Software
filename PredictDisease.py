# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
# Qt相关


from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from SampleClass import SampleClass #分析样本类别
from PredictResult import PredictResult
# 加载UI
from UI.Ui_PredictWindow import Ui_Dialog_predict

# 导入配置文件
from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import pickle
import numpy as np
import pandas as pd
from xgboost import XGBClassifier as XGBC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix as cm, roc_auc_score as auc

# 添加新样品类


class PredictDisease(QDialog):
    # 发出信号(类型是list)
    data_update_signal = pyqtSignal(list)
    # 把当前位置location串进来了

    def __init__(self, parent=None, patient_id=None):
        super(PredictDisease, self).__init__(parent)
        # ui初始化
        self.__UI = Ui_Dialog_predict()
        self.__UI.setupUi(self)
        self.__UI.lineEdit_pID.setText(patient_id)

        self.title=""
        self.result = 0
        self.x_column = None
        self.type = None
        self.get_predict_type()

        self.data = None
        self.connection = None
        self.cursor = None
        self.logger = None
        self.set_connection_cursor()
        self.set_logger()

    # 单击【提交】按钮槽函数

    @pyqtSlot()
    def on_btn_confirm_clicked(self):
        # 取数据
        self.get_data()
        # 加载与训练模型
        if self.type == '新冠':
            f = open('model/covid19.pickle', 'rb')
            model = pickle.load(f)
            f.close()

        # todo:
        # predict
        predict_df = pd.DataFrame(columns=self.x_column)
        predict_df.loc[0] = self.data
        predict_df = predict_df.astype("float")
        # 预测
        r = model.predict_proba(predict_df)
        self.result = r[0, 1]

        #新窗口
        result_dialog = PredictResult(self,self.result,self.title)
        result_dialog.setAttribute(Qt.WA_DeleteOnClose)
        result_dialog.show()

    def get_data(self):
        # 病人编号
        pID = self.__UI.lineEdit_pID.text()
        sql = ""
        # 得到sql
        if self.type == '新冠':
            sql = """SELECT respiratory_rate,lactate,diastolic,sistolic,neutrophiles,oxyden_saturation,hemoglobin,urea,dimer,platelets,hemetocrite
                    FROM exam_result WHERE patient_ID='%s' """ % pID
        # 取数据
        self.cursor.execute(sql)
        self.connection.commit()
        data_list = list(self.cursor.fetchall()[0])
        # list
        self.data = data_list

    # 设置cursor和connection

    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    def get_predict_type(self):
        self.type = self.__UI.comboBox_type.currentText()
        if self.type == '新冠':
            print("新冠来了")
            self.title='患有严重新冠的可能性'
            self.x_column = [
                'RESPIRATORY_RATE_MEAN',
                'LACTATE_MEAN',
                'BLOODPRESSURE_DIASTOLIC_MEAN',
                'BLOODPRESSURE_SISTOLIC_MEAN',
                'NEUTROPHILES_MEAN',
                'OXYGEN_SATURATION_MEAN',
                'HEMOGLOBIN_MEAN',
                'UREA_MEAN',
                'DIMER_MEAN',
                'PLATELETS_MEAN',
                'HEMATOCRITE_MEAN']
