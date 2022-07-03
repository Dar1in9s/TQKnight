from PyQt5.QtWidgets import QWidget, QDialog, QAbstractItemView, QTableWidget, QMenu, QAction, QMessageBox, \
    QTableWidgetItem, QDialogButtonBox
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from View.ProxyWindow.UI import Ui_ProxyWindow, Ui_ProxyInfo
from Model.SQLModelObject import Proxy


class ProxyWindow(QWidget, Ui_ProxyWindow):
    signalAddProxy = pyqtSignal(Proxy)
    signalModifyProxy = pyqtSignal(Proxy)
    signalDeleteProxy = pyqtSignal(int)
    signalRefreshProxy = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ProxyWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.tableWidget_proxy.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_proxy.verticalHeader().setVisible(False)
        self.tableWidget_proxy.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_proxy.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_proxy.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_proxy.setColumnCount(6)
        self.tableWidget_proxy.setHorizontalHeaderLabels(["名字", "类型", "主机", "端口", "用户名", "密码"])

        self.tableWidget_proxy.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_proxy.customContextMenuRequested.connect(self.showMenu)
        self.tableWidget_proxy.doubleClicked.connect(self.actionModifyProxyClicked)

    def showMenu(self):
        menu = QMenu(self)
        actionAddProxy = QAction("添加")
        actionAddProxy.triggered.connect(self.actionAddProxyClicked)
        actionModifyProxy = QAction("修改")
        actionModifyProxy.triggered.connect(self.actionModifyProxyClicked)
        actionDeleteProxy = QAction("删除")
        actionDeleteProxy.triggered.connect(self.actionDeleteProxyClicked)
        if not self.tableWidget_proxy.currentItem():
            actionModifyProxy.setEnabled(False)
            actionDeleteProxy.setEnabled(False)

        menu.addAction(actionAddProxy)
        menu.addAction(actionModifyProxy)
        menu.addAction(actionDeleteProxy)
        menu.exec_(QCursor.pos())

    def showProxies(self, proxies):
        for proxyObj in proxies:
            if proxyObj.id == 0:
                continue
            row = self.tableWidget_proxy.rowCount()
            self.tableWidget_proxy.setRowCount(row + 1)
            self.tableWidget_proxy.setVerticalHeaderItem(row, QTableWidgetItem(str(proxyObj.id)))
            self.tableWidget_proxy.setItem(row, 0, QTableWidgetItem(proxyObj.name))
            self.tableWidget_proxy.setItem(row, 1, QTableWidgetItem(proxyObj.protocol))
            self.tableWidget_proxy.setItem(row, 2, QTableWidgetItem(proxyObj.server))
            self.tableWidget_proxy.setItem(row, 3, QTableWidgetItem(proxyObj.port))
            self.tableWidget_proxy.setItem(row, 4, QTableWidgetItem(proxyObj.user))
            self.tableWidget_proxy.setItem(row, 5, QTableWidgetItem(proxyObj.passwd))
            self.tableWidget_proxy.resizeRowsToContents()

    def actionAddProxyClicked(self):
        proxyInfo = ProxyInfo()
        if proxyInfo.exec_() == QDialog.Accepted:
            proxyObj = Proxy()
            proxyObj.name = proxyInfo.lineEdit_name.text().strip()
            proxyObj.protocol = proxyInfo.comboBox_type.currentText().strip()
            proxyObj.server = proxyInfo.lineEdit_host.text().strip()
            proxyObj.port = proxyInfo.spinBox_port.value()
            proxyObj.user = proxyInfo.lineEdit_user.text().strip()
            proxyObj.passwd = proxyInfo.lineEdit_passwd.text().strip()
            self.signalAddProxy.emit(proxyObj)

    def addProxyResult(self, result):
        if result["status"] == "error":
            return QMessageBox.warning(self, "提示", result["message"])
        self.showProxies(result["proxyObj"])

    def actionModifyProxyClicked(self):
        proxyInfo = ProxyInfo()
        row = self.tableWidget_proxy.currentRow()
        proxyInfo.lineEdit_name.setText(self.tableWidget_proxy.item(row, 0).text())
        proxyInfo.comboBox_type.setCurrentText(self.tableWidget_proxy.item(row, 1).text())
        proxyInfo.lineEdit_host.setText(self.tableWidget_proxy.item(row, 2).text())
        proxyInfo.spinBox_port.setValue(int(self.tableWidget_proxy.item(row, 3).text()))
        proxyInfo.lineEdit_user.setText(self.tableWidget_proxy.item(row, 4).text())
        proxyInfo.lineEdit_passwd.setText(self.tableWidget_proxy.item(row, 5).text())
        if proxyInfo.exec_() == QDialog.Accepted:
            proxyObj = Proxy()
            proxyObj.id = int(self.tableWidget_proxy.verticalHeaderItem(row).text())
            proxyObj.name = proxyInfo.lineEdit_name.text().strip()
            proxyObj.protocol = proxyInfo.comboBox_type.currentText().strip()
            proxyObj.server = proxyInfo.lineEdit_host.text().strip()
            proxyObj.port = proxyInfo.spinBox_port.value()
            proxyObj.user = proxyInfo.lineEdit_user.text().strip()
            proxyObj.passwd = proxyInfo.lineEdit_passwd.text().strip()
            self.signalModifyProxy.emit(proxyObj)

    def modifyProxyResult(self, result):
        if result["status"] == "noModify":
            return
        if result["status"] == "error":
            return QMessageBox.warning(self, "提示", result["message"])
        proxyObj = result["proxyObj"]
        row = self.tableWidget_proxy.currentRow()
        self.tableWidget_proxy.item(row, 0).setText(proxyObj.name)
        self.tableWidget_proxy.item(row, 1).setText(proxyObj.protocol)
        self.tableWidget_proxy.item(row, 2).setText(proxyObj.server)
        self.tableWidget_proxy.item(row, 3).setText(str(proxyObj.port))
        self.tableWidget_proxy.item(row, 4).setText(proxyObj.user)
        self.tableWidget_proxy.item(row, 5).setText(proxyObj.passwd)

    def actionDeleteProxyClicked(self):
        row = self.tableWidget_proxy.currentRow()
        dId = int(self.tableWidget_proxy.verticalHeaderItem(row).text())
        self.signalDeleteProxy.emit(dId)

    def deleteProxyResult(self, result):
        if result["status"] == "error":
            return QMessageBox.warning(self, "提示", result["message"])
        self.tableWidget_proxy.removeRow(self.tableWidget_proxy.currentRow())


class ProxyInfo(QDialog, Ui_ProxyInfo):
    def __init__(self, *args, **kwargs):
        super(ProxyInfo, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Ok).setIcon(QIcon(":/proxy/ok.png"))
        self.buttonBox.button(QDialogButtonBox.Cancel).setIcon(QIcon(":/proxy/cancel.png"))

    def clearAll(self):
        self.lineEdit_passwd.clear()
        self.lineEdit_name.clear()
        self.lineEdit_host.clear()
        self.lineEdit_user.clear()
        self.comboBox_type.setCurrentIndex(0)
        self.spinBox_port.setValue("1080")

    def accept(self):
        if not self.lineEdit_name.text().strip():
            return QMessageBox.warning(self, "提示", "名字不能为空")
        if not self.lineEdit_host.text().strip():
            return QMessageBox.warning(self, "提示", "主机不能为空")
        if not self.spinBox_port.value():
            return QMessageBox.warning(self, "提示", "端口不能为空")
        super().accept()
