# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataBaseResultInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatabaseResultInfo(object):
    def setupUi(self, DatabaseResultInfo):
        DatabaseResultInfo.setObjectName("DatabaseResultInfo")
        DatabaseResultInfo.resize(746, 488)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(DatabaseResultInfo)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(DatabaseResultInfo)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_attr = QtWidgets.QWidget()
        self.tab_attr.setObjectName("tab_attr")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_attr)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget_attr = QtWidgets.QTableWidget(self.tab_attr)
        self.tableWidget_attr.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_attr.setDragEnabled(False)
        self.tableWidget_attr.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_attr.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_attr.setObjectName("tableWidget_attr")
        self.tableWidget_attr.setColumnCount(0)
        self.tableWidget_attr.setRowCount(0)
        self.tableWidget_attr.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget_attr)
        self.tabWidget.addTab(self.tab_attr, "")
        self.tab_data = QtWidgets.QWidget()
        self.tab_data.setObjectName("tab_data")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_data)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableWidget_data = QtWidgets.QTableWidget(self.tab_data)
        self.tableWidget_data.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_data.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_data.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_data.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_data.setObjectName("tableWidget_data")
        self.tableWidget_data.setColumnCount(0)
        self.tableWidget_data.setRowCount(0)
        self.tableWidget_data.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_3.addWidget(self.tableWidget_data)
        self.tabWidget.addTab(self.tab_data, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(DatabaseResultInfo)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DatabaseResultInfo)

    def retranslateUi(self, DatabaseResultInfo):
        _translate = QtCore.QCoreApplication.translate
        DatabaseResultInfo.setWindowTitle(_translate("DatabaseResultInfo", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_attr), _translate("DatabaseResultInfo", "??????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), _translate("DatabaseResultInfo", "??????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatabaseResultInfo = QtWidgets.QWidget()
    ui = Ui_DatabaseResultInfo()
    ui.setupUi(DatabaseResultInfo)
    DatabaseResultInfo.show()
    sys.exit(app.exec_())
