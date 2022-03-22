# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PredictWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_predict(object):
    def setupUi(self, Dialog_predict):
        Dialog_predict.setObjectName("Dialog_predict")
        Dialog_predict.resize(700, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_predict.sizePolicy().hasHeightForWidth())
        Dialog_predict.setSizePolicy(sizePolicy)
        Dialog_predict.setMinimumSize(QtCore.QSize(700, 600))
        self.btn_confirm = QtWidgets.QPushButton(Dialog_predict)
        self.btn_confirm.setGeometry(QtCore.QRect(10, 470, 113, 32))
        self.btn_confirm.setStyleSheet("font: 13pt \"Hei\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/pictures/navigation-000-button-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_confirm.setIcon(icon)
        self.btn_confirm.setObjectName("btn_confirm")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog_predict)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 160, 118))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_pID = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_pID.setObjectName("lineEdit_pID")
        self.verticalLayout.addWidget(self.lineEdit_pID)
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox_type = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.verticalLayout.addWidget(self.comboBox_type)

        self.retranslateUi(Dialog_predict)
        QtCore.QMetaObject.connectSlotsByName(Dialog_predict)

    def retranslateUi(self, Dialog_predict):
        _translate = QtCore.QCoreApplication.translate
        Dialog_predict.setWindowTitle(_translate("Dialog_predict", "疾病风险预测"))
        self.btn_confirm.setText(_translate("Dialog_predict", "确定"))
        self.label.setText(_translate("Dialog_predict", "输入病人编号"))
        self.label_2.setText(_translate("Dialog_predict", "预测疾病种类"))
        self.comboBox_type.setItemText(0, _translate("Dialog_predict", "VWD类型"))
        self.comboBox_type.setItemText(1, _translate("Dialog_predict", "新冠"))
        self.comboBox_type.setItemText(2, _translate("Dialog_predict", "血友病"))
        self.comboBox_type.setItemText(3, _translate("Dialog_predict", "血小板减少症"))
        self.comboBox_type.setItemText(4, _translate("Dialog_predict", "急性白血病"))
        self.comboBox_type.setItemText(5, _translate("Dialog_predict", "血栓"))
import creat_rc
