# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProxyInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProxyInfo(object):
    def setupUi(self, ProxyInfo):
        ProxyInfo.setObjectName("ProxyInfo")
        ProxyInfo.resize(360, 300)
        ProxyInfo.setMinimumSize(QtCore.QSize(360, 300))
        ProxyInfo.setMaximumSize(QtCore.QSize(360, 300))
        self.gridLayout = QtWidgets.QGridLayout(ProxyInfo)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ProxyInfo)
        self.label.setMinimumSize(QtCore.QSize(2, 0))
        self.label.setMaximumSize(QtCore.QSize(55, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(ProxyInfo)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ProxyInfo)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox_type = QtWidgets.QComboBox(ProxyInfo)
        self.comboBox_type.setMinimumSize(QtCore.QSize(100, 30))
        self.comboBox_type.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.gridLayout.addWidget(self.comboBox_type, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ProxyInfo)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_host = QtWidgets.QLineEdit(ProxyInfo)
        self.lineEdit_host.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridLayout.addWidget(self.lineEdit_host, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(ProxyInfo)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.spinBox_port = QtWidgets.QSpinBox(ProxyInfo)
        self.spinBox_port.setMinimumSize(QtCore.QSize(0, 30))
        self.spinBox_port.setMaximumSize(QtCore.QSize(100, 30))
        self.spinBox_port.setMinimum(1)
        self.spinBox_port.setMaximum(65535)
        self.spinBox_port.setObjectName("spinBox_port")
        self.gridLayout.addWidget(self.spinBox_port, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(ProxyInfo)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEdit_user = QtWidgets.QLineEdit(ProxyInfo)
        self.lineEdit_user.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.gridLayout.addWidget(self.lineEdit_user, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(ProxyInfo)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.lineEdit_passwd = QtWidgets.QLineEdit(ProxyInfo)
        self.lineEdit_passwd.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_passwd.setObjectName("lineEdit_passwd")
        self.gridLayout.addWidget(self.lineEdit_passwd, 5, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ProxyInfo)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)

        self.retranslateUi(ProxyInfo)
        self.buttonBox.accepted.connect(ProxyInfo.accept)
        self.buttonBox.rejected.connect(ProxyInfo.reject)
        QtCore.QMetaObject.connectSlotsByName(ProxyInfo)

    def retranslateUi(self, ProxyInfo):
        _translate = QtCore.QCoreApplication.translate
        ProxyInfo.setWindowTitle(_translate("ProxyInfo", "代理设置"))
        self.label.setText(_translate("ProxyInfo", "名字："))
        self.label_2.setText(_translate("ProxyInfo", "类型："))
        self.comboBox_type.setItemText(0, _translate("ProxyInfo", "http"))
        self.comboBox_type.setItemText(1, _translate("ProxyInfo", "socks"))
        self.label_3.setText(_translate("ProxyInfo", "主机："))
        self.label_4.setText(_translate("ProxyInfo", "端口："))
        self.label_5.setText(_translate("ProxyInfo", "用户名："))
        self.label_6.setText(_translate("ProxyInfo", "密码："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProxyInfo = QtWidgets.QDialog()
    ui = Ui_ProxyInfo()
    ui.setupUi(ProxyInfo)
    ProxyInfo.show()
    sys.exit(app.exec_())