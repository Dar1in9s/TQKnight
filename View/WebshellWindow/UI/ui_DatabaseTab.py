# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatabaseTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatabaseTab(object):
    def setupUi(self, DatabaseInfo):
        DatabaseInfo.setObjectName("DatabaseInfo")
        DatabaseInfo.resize(1110, 606)
        self.verticalLayout = QtWidgets.QVBoxLayout(DatabaseInfo)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(DatabaseInfo)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_type = QtWidgets.QComboBox(self.widget)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_type)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_host = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_host.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.horizontalLayout.addWidget(self.lineEdit_host)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_port = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_port.setMinimumSize(QtCore.QSize(70, 0))
        self.lineEdit_port.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout.addWidget(self.lineEdit_port)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.lineEdit_database = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_database.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_database.setObjectName("lineEdit_database")
        self.horizontalLayout.addWidget(self.lineEdit_database)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEdit_user = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_user.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.horizontalLayout.addWidget(self.lineEdit_user)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.lineEdit_passwd = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_passwd.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_passwd.setObjectName("lineEdit_passwd")
        self.horizontalLayout.addWidget(self.lineEdit_passwd)
        self.btn_connect = QtWidgets.QPushButton(self.widget)
        self.btn_connect.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_connect.setMaximumSize(QtCore.QSize(59, 16777215))
        self.btn_connect.setObjectName("btn_connect")
        self.horizontalLayout.addWidget(self.btn_connect)
        self.btn_sql = QtWidgets.QPushButton(self.widget)
        self.btn_sql.setObjectName("btn_sql")
        self.horizontalLayout.addWidget(self.btn_sql)
        self.verticalLayout.addWidget(self.widget)
        self.widget_main = QtWidgets.QWidget(DatabaseInfo)
        self.widget_main.setObjectName("widget_main")
        self.layout_main = QtWidgets.QHBoxLayout(self.widget_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)
        self.layout_main.setObjectName("layout_main")
        self.verticalLayout.addWidget(self.widget_main)

        self.retranslateUi(DatabaseInfo)
        QtCore.QMetaObject.connectSlotsByName(DatabaseInfo)

    def retranslateUi(self, DatabaseInfo):
        _translate = QtCore.QCoreApplication.translate
        DatabaseInfo.setWindowTitle(_translate("DatabaseInfo", "Form"))
        self.label.setText(_translate("DatabaseInfo", "数据库类型："))
        self.comboBox_type.setItemText(0, _translate("DatabaseInfo", "mysql"))
        self.label_2.setText(_translate("DatabaseInfo", "服务器地址："))
        self.lineEdit_host.setText(_translate("DatabaseInfo", "127.0.0.1"))
        self.label_3.setText(_translate("DatabaseInfo", "端口："))
        self.lineEdit_port.setText(_translate("DatabaseInfo", "3306"))
        self.label_4.setText(_translate("DatabaseInfo", "数据库："))
        self.lineEdit_database.setText(_translate("DatabaseInfo", "mysql"))
        self.label_5.setText(_translate("DatabaseInfo", "用户名："))
        self.lineEdit_user.setText(_translate("DatabaseInfo", "root"))
        self.label_6.setText(_translate("DatabaseInfo", "密码："))
        self.lineEdit_passwd.setText(_translate("DatabaseInfo", "root"))
        self.btn_connect.setText(_translate("DatabaseInfo", "连接"))
        self.btn_sql.setText(_translate("DatabaseInfo", "自定义sql"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatabaseInfo = QtWidgets.QWidget()
    ui = Ui_DatabaseTab()
    ui.setupUi(DatabaseInfo)
    DatabaseInfo.show()
    sys.exit(app.exec_())