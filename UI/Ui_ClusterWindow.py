# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClusterWindow.ui'
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 110, 366, 199))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.cb_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_cb.setObjectName("cb_cb")
        self.gridLayout.addWidget(self.cb_cb, 1, 2, 1, 1)
        self.cb_act = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_act.setObjectName("cb_act")
        self.gridLayout.addWidget(self.cb_act, 0, 2, 1, 1)
        self.cb_fv3c = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_fv3c.setObjectName("cb_fv3c")
        self.gridLayout.addWidget(self.cb_fv3c, 1, 0, 1, 1)
        self.btn_confirm = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_confirm.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.btn_confirm.setObjectName("btn_confirm")
        self.gridLayout.addWidget(self.btn_confirm, 3, 0, 1, 1)
        self.cb_age = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_age.setObjectName("cb_age")
        self.gridLayout.addWidget(self.cb_age, 2, 2, 1, 1)
        self.cb_aptt = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_aptt.setObjectName("cb_aptt")
        self.gridLayout.addWidget(self.cb_aptt, 0, 0, 1, 1)
        self.cb_bs = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_bs.setObjectName("cb_bs")
        self.gridLayout.addWidget(self.cb_bs, 2, 0, 1, 1)
        self.cb_ag = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_ag.setObjectName("cb_ag")
        self.gridLayout.addWidget(self.cb_ag, 0, 1, 1, 1)
        self.cb_ripa = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_ripa.setObjectName("cb_ripa")
        self.gridLayout.addWidget(self.cb_ripa, 1, 1, 1, 1)
        self.cb_pp = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_pp.setObjectName("cb_pp")
        self.gridLayout.addWidget(self.cb_pp, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 50, 108, 89))
        self.label.setStyleSheet("font: 13pt \"Heiti SC\";")
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "聚类分析"))
        self.cb_cb.setText(_translate("Dialog", "CB"))
        self.cb_act.setText(_translate("Dialog", "Act"))
        self.cb_fv3c.setText(_translate("Dialog", "FV3C"))
        self.btn_confirm.setText(_translate("Dialog", "确定"))
        self.cb_age.setText(_translate("Dialog", "Age"))
        self.cb_aptt.setText(_translate("Dialog", "APTT"))
        self.cb_bs.setText(_translate("Dialog", "BS"))
        self.cb_ag.setText(_translate("Dialog", "Ag"))
        self.cb_ripa.setText(_translate("Dialog", "RIPA"))
        self.cb_pp.setText(_translate("Dialog", "pp"))
        self.label.setText(_translate("Dialog", "选择要纳入的指标"))
import creat_rc
