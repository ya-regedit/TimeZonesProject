# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 318)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.statusbar = QtWidgets.QLabel(Form)
        self.statusbar.setText("")
        self.statusbar.setObjectName("statusbar")
        self.verticalLayout.addWidget(self.statusbar)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setMinimumSize(QtCore.QSize(179, 0))
        self.clear.setObjectName("clear")
        self.horizontalLayout.addWidget(self.clear)
        self.get_info = QtWidgets.QPushButton(Form)
        self.get_info.setObjectName("get_info")
        self.horizontalLayout.addWidget(self.get_info)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "History of requests"))
        self.clear.setText(_translate("Form", "Clear history"))
        self.get_info.setText(_translate("Form", "Get information about requests"))
