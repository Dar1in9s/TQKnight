# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WebshellWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WebshellWindow(object):
    def setupUi(self, WebshellWindow):
        WebshellWindow.setObjectName("WebshellWindow")
        WebshellWindow.resize(1347, 768)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WebshellWindow)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(WebshellWindow)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_info = QtWidgets.QWidget()
        self.tab_info.setObjectName("tab_info")
        self.layout_info = QtWidgets.QHBoxLayout(self.tab_info)
        self.layout_info.setContentsMargins(0, 0, 0, 0)
        self.layout_info.setSpacing(0)
        self.layout_info.setObjectName("layout_info")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/other/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_info, icon, "")
        self.tab_file = QtWidgets.QWidget()
        self.tab_file.setObjectName("tab_file")
        self.layout_file = QtWidgets.QHBoxLayout(self.tab_file)
        self.layout_file.setContentsMargins(0, 0, 0, 0)
        self.layout_file.setSpacing(0)
        self.layout_file.setObjectName("layout_file")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/other/fileManage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_file, icon1, "")
        self.tab_shell = QtWidgets.QWidget()
        self.tab_shell.setObjectName("tab_shell")
        self.layout_shell = QtWidgets.QHBoxLayout(self.tab_shell)
        self.layout_shell.setContentsMargins(0, 0, 0, 0)
        self.layout_shell.setSpacing(0)
        self.layout_shell.setObjectName("layout_shell")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/other/shell.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_shell, icon2, "")
        self.tab_dbs = QtWidgets.QWidget()
        self.tab_dbs.setObjectName("tab_dbs")
        self.layout_database = QtWidgets.QHBoxLayout(self.tab_dbs)
        self.layout_database.setContentsMargins(0, 0, 0, 0)
        self.layout_database.setSpacing(0)
        self.layout_database.setObjectName("layout_database")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/other/database.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_dbs, icon3, "")
        self.tab_proxy = QtWidgets.QWidget()
        self.tab_proxy.setObjectName("tab_proxy")
        self.layout_IntranetProxy = QtWidgets.QHBoxLayout(self.tab_proxy)
        self.layout_IntranetProxy.setContentsMargins(0, 0, 0, 0)
        self.layout_IntranetProxy.setSpacing(0)
        self.layout_IntranetProxy.setObjectName("layout_IntranetProxy")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/other/intranet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_proxy, icon4, "")
        self.tab_plugin = QtWidgets.QWidget()
        self.tab_plugin.setObjectName("tab_plugin")
        self.layout_plugin = QtWidgets.QHBoxLayout(self.tab_plugin)
        self.layout_plugin.setContentsMargins(0, 0, 0, 0)
        self.layout_plugin.setSpacing(0)
        self.layout_plugin.setObjectName("layout_plugin")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/other/plug.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_plugin, icon5, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(WebshellWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WebshellWindow)

    def retranslateUi(self, WebshellWindow):
        _translate = QtCore.QCoreApplication.translate
        WebshellWindow.setWindowTitle(_translate("WebshellWindow", "TQKnight"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_info), _translate("WebshellWindow", "Webshell信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_file), _translate("WebshellWindow", "文件管理"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_shell), _translate("WebshellWindow", "虚拟终端"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_dbs), _translate("WebshellWindow", "数据库管理"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_proxy), _translate("WebshellWindow", "内网穿透"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plugin), _translate("WebshellWindow", "插件"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WebshellWindow = QtWidgets.QWidget()
    ui = Ui_WebshellWindow()
    ui.setupUi(WebshellWindow)
    WebshellWindow.show()
    sys.exit(app.exec_())
