# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateSampleWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(464, 237)
        self.btn_commit = QtWidgets.QPushButton(Dialog)
        self.btn_commit.setGeometry(QtCore.QRect(30, 180, 93, 28))
        self.btn_commit.setObjectName("btn_commit")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 40, 398, 135))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.lineEdit_ID = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_ID.setText("")
        self.lineEdit_ID.setObjectName("lineEdit_ID")
        self.gridLayout.addWidget(self.lineEdit_ID, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.comboBox_sample_type = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_sample_type.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_sample_type.setObjectName("comboBox_sample_type")
        self.comboBox_sample_type.addItem("")
        self.comboBox_sample_type.addItem("")
        self.gridLayout.addWidget(self.comboBox_sample_type, 3, 0, 2, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 1, 0, 1, 1)
        self.lineEdit_sample_size = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_sample_size.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_sample_size.setText("")
        self.lineEdit_sample_size.setObjectName("lineEdit_sample_size")
        self.gridLayout.addWidget(self.lineEdit_sample_size, 3, 2, 2, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "创建样本"))
        self.btn_commit.setText(_translate("Dialog", "提交"))
        self.label_4.setText(_translate("Dialog", "样本量"))
        self.label_2.setText(_translate("Dialog", "样本编号"))
        self.lineEdit_ID.setPlaceholderText(_translate("Dialog", "编号"))
        self.label_3.setText(_translate("Dialog", "样本类型"))
        self.comboBox_sample_type.setItemText(0, _translate("Dialog", "血浆"))
        self.comboBox_sample_type.setItemText(1, _translate("Dialog", "血细胞"))
        self.label.setText(_translate("Dialog", "姓名"))
        self.lineEdit_name.setPlaceholderText(_translate("Dialog", "姓名"))
        self.lineEdit_sample_size.setPlaceholderText(
            _translate("Dialog", "样本量"))
