# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CorWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(600, 500))
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 70, 366, 199))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_confirm = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_confirm.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.btn_confirm.setObjectName("btn_confirm")
        self.gridLayout.addWidget(self.btn_confirm, 5, 0, 1, 1)
        self.cb2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb2.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.cb2.setObjectName("cb2")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.cb2.addItem("")
        self.gridLayout.addWidget(self.cb2, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.cb1 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb1.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.cb1.setObjectName("cb1")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.cb1.addItem("")
        self.gridLayout.addWidget(self.cb1, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.btn_help = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_help.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.btn_help.setObjectName("btn_help")
        self.gridLayout.addWidget(self.btn_help, 0, 0, 1, 1)
        self.cb_method = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cb_method.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.cb_method.setObjectName("cb_method")
        self.cb_method.addItem("")
        self.cb_method.addItem("")
        self.cb_method.addItem("")
        self.gridLayout.addWidget(self.cb_method, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.lable_value = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lable_value.setStyleSheet("font: 13pt \"Heiti SC\";\n"
"font: 13pt \".AppleSystemUIFont\";")
        self.lable_value.setText("")
        self.lable_value.setObjectName("lable_value")
        self.gridLayout.addWidget(self.lable_value, 6, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "相关性分析"))
        self.btn_confirm.setText(_translate("Dialog", "确定"))
        self.cb2.setItemText(0, _translate("Dialog", "年龄"))
        self.cb2.setItemText(1, _translate("Dialog", "APTT"))
        self.cb2.setItemText(2, _translate("Dialog", "Ag"))
        self.cb2.setItemText(3, _translate("Dialog", "Act"))
        self.cb2.setItemText(4, _translate("Dialog", "RIPA"))
        self.cb2.setItemText(5, _translate("Dialog", "CB"))
        self.cb2.setItemText(6, _translate("Dialog", "血糖"))
        self.cb2.setItemText(7, _translate("Dialog", "乳酸"))
        self.cb2.setItemText(8, _translate("Dialog", "中性粒细胞"))
        self.cb2.setItemText(9, _translate("Dialog", "血红蛋白"))
        self.cb2.setItemText(10, _translate("Dialog", "尿素"))
        self.cb2.setItemText(11, _translate("Dialog", "二聚体"))
        self.cb2.setItemText(12, _translate("Dialog", "血红素"))
        self.cb2.setItemText(13, _translate("Dialog", "舒张压"))
        self.cb2.setItemText(14, _translate("Dialog", "收缩压"))
        self.cb2.setItemText(15, _translate("Dialog", "血氧饱和度"))
        self.cb2.setItemText(16, _translate("Dialog", "血小板"))
        self.label_2.setText(_translate("Dialog", "选择方法"))
        self.cb1.setItemText(0, _translate("Dialog", "年龄"))
        self.cb1.setItemText(1, _translate("Dialog", "APTT"))
        self.cb1.setItemText(2, _translate("Dialog", "Ag"))
        self.cb1.setItemText(3, _translate("Dialog", "Act"))
        self.cb1.setItemText(4, _translate("Dialog", "RIPA"))
        self.cb1.setItemText(5, _translate("Dialog", "CB"))
        self.cb1.setItemText(6, _translate("Dialog", "血糖"))
        self.cb1.setItemText(7, _translate("Dialog", "乳酸"))
        self.cb1.setItemText(8, _translate("Dialog", "中性粒细胞"))
        self.cb1.setItemText(9, _translate("Dialog", "血红蛋白"))
        self.cb1.setItemText(10, _translate("Dialog", "尿素"))
        self.cb1.setItemText(11, _translate("Dialog", "二聚体"))
        self.cb1.setItemText(12, _translate("Dialog", "血红素"))
        self.cb1.setItemText(13, _translate("Dialog", "舒张压"))
        self.cb1.setItemText(14, _translate("Dialog", "收缩压"))
        self.cb1.setItemText(15, _translate("Dialog", "血氧饱和度"))
        self.cb1.setItemText(16, _translate("Dialog", "血小板"))
        self.label.setText(_translate("Dialog", "选择要观察的指标"))
        self.btn_help.setText(_translate("Dialog", "查看提示"))
        self.cb_method.setItemText(0, _translate("Dialog", "Pearson"))
        self.cb_method.setItemText(1, _translate("Dialog", "Spearman"))
        self.cb_method.setItemText(2, _translate("Dialog", "Kendall"))
        self.label_3.setText(_translate("Dialog", "相关系数"))
import creat_rc
