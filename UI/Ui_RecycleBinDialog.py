# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RecycleBinDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecycleBinDialog(object):
    def setupUi(self, RecycleBinDialog):
        RecycleBinDialog.setObjectName("RecycleBinDialog")
        RecycleBinDialog.resize(893, 806)
        self.tableView = QtWidgets.QTableView(RecycleBinDialog)
        self.tableView.setGeometry(QtCore.QRect(50, 110, 801, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(0, 600))
        self.tableView.setObjectName("tableView")
        self.label = QtWidgets.QLabel(RecycleBinDialog)
        self.label.setGeometry(QtCore.QRect(410, 70, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Hei")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(RecycleBinDialog)
        QtCore.QMetaObject.connectSlotsByName(RecycleBinDialog)

    def retranslateUi(self, RecycleBinDialog):
        _translate = QtCore.QCoreApplication.translate
        RecycleBinDialog.setWindowTitle(_translate("RecycleBinDialog", "回收站"))
        self.label.setText(_translate("RecycleBinDialog", "回收站样本"))
