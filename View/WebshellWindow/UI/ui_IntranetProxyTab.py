# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IntranetProxyTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IntranetProxyTab(object):
    def setupUi(self, IntranetProxyTab):
        IntranetProxyTab.setObjectName("IntranetProxyTab")
        IntranetProxyTab.resize(951, 530)
        IntranetProxyTab.setStyleSheet("QPushButton{\n"
"    border-image: url(:/webshell/closed.png);\n"
"}\n"
"QPushButton:checked{\n"
"    border-image: url(:/webshell/opened.png);\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(IntranetProxyTab)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(IntranetProxyTab)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_bind = QtWidgets.QWidget()
        self.tab_bind.setObjectName("tab_bind")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_bind)
        self.verticalLayout.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_bind)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(20, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox_bindHttpPort = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_bindHttpPort.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox_bindHttpPort.setMinimum(1)
        self.spinBox_bindHttpPort.setMaximum(65535)
        self.spinBox_bindHttpPort.setProperty("value", 1024)
        self.spinBox_bindHttpPort.setDisplayIntegerBase(10)
        self.spinBox_bindHttpPort.setObjectName("spinBox_bindHttpPort")
        self.gridLayout.addWidget(self.spinBox_bindHttpPort, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btn_bindHttp = QtWidgets.QPushButton(self.groupBox)
        self.btn_bindHttp.setMinimumSize(QtCore.QSize(60, 60))
        self.btn_bindHttp.setMaximumSize(QtCore.QSize(60, 60))
        self.btn_bindHttp.setText("")
        self.btn_bindHttp.setCheckable(True)
        self.btn_bindHttp.setObjectName("btn_bindHttp")
        self.gridLayout.addWidget(self.btn_bindHttp, 0, 4, 2, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_bind)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setContentsMargins(11, 5, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit_bindLog = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_bindLog.setMinimumSize(QtCore.QSize(0, 75))
        self.textEdit_bindLog.setReadOnly(True)
        self.textEdit_bindLog.setObjectName("textEdit_bindLog")
        self.horizontalLayout_2.addWidget(self.textEdit_bindLog)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tab_bind, "")
        self.tab_reverse = QtWidgets.QWidget()
        self.tab_reverse.setObjectName("tab_reverse")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_reverse)
        self.verticalLayout_2.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_reverse)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 2, 1, 1)
        self.spinBox_reversePort = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_reversePort.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox_reversePort.setMinimum(1)
        self.spinBox_reversePort.setMaximum(65535)
        self.spinBox_reversePort.setProperty("value", 1024)
        self.spinBox_reversePort.setDisplayIntegerBase(10)
        self.spinBox_reversePort.setObjectName("spinBox_reversePort")
        self.gridLayout_3.addWidget(self.spinBox_reversePort, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit_reverseIp = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_reverseIp.setObjectName("lineEdit_reverseIp")
        self.gridLayout_3.addWidget(self.lineEdit_reverseIp, 0, 1, 1, 1)
        self.btn_reverse = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_reverse.setMinimumSize(QtCore.QSize(60, 60))
        self.btn_reverse.setMaximumSize(QtCore.QSize(60, 60))
        self.btn_reverse.setText("")
        self.btn_reverse.setCheckable(True)
        self.btn_reverse.setObjectName("btn_reverse")
        self.gridLayout_3.addWidget(self.btn_reverse, 0, 5, 2, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 5)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_reverse)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textEdit_reverseLog = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEdit_reverseLog.setReadOnly(True)
        self.textEdit_reverseLog.setObjectName("textEdit_reverseLog")
        self.verticalLayout_3.addWidget(self.textEdit_reverseLog)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.tabWidget.addTab(self.tab_reverse, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(IntranetProxyTab)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IntranetProxyTab)

    def retranslateUi(self, IntranetProxyTab):
        _translate = QtCore.QCoreApplication.translate
        IntranetProxyTab.setWindowTitle(_translate("IntranetProxyTab", "Form"))
        self.groupBox.setTitle(_translate("IntranetProxyTab", "配置"))
        self.label.setText(_translate("IntranetProxyTab", "本地监听端口："))
        self.label_2.setText(_translate("IntranetProxyTab", "本地开启一个端口，将本地端口映射到服务器，本地端口作为socks连接端口"))
        self.groupBox_3.setTitle(_translate("IntranetProxyTab", "连接日志"))
        self.textEdit_bindLog.setHtml(_translate("IntranetProxyTab", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_bind), _translate("IntranetProxyTab", "正向代理"))
        self.groupBox_4.setTitle(_translate("IntranetProxyTab", "配置"))
        self.label_6.setText(_translate("IntranetProxyTab", "VPS端口："))
        self.label_5.setText(_translate("IntranetProxyTab", "VPS地址："))
        self.label_7.setText(_translate("IntranetProxyTab", "服务器将主动连接VPS的指定端口，构成Socks隧道"))
        self.groupBox_5.setTitle(_translate("IntranetProxyTab", "连接日志"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_reverse), _translate("IntranetProxyTab", "反向代理"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IntranetProxyTab = QtWidgets.QWidget()
    ui = Ui_IntranetProxyTab()
    ui.setupUi(IntranetProxyTab)
    IntranetProxyTab.show()
    sys.exit(app.exec_())