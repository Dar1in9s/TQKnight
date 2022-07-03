from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from View.WebshellWindow.UI import Ui_IntranetProxyTab


class IntranetProxyTab(QWidget, Ui_IntranetProxyTab):
    signalHttpSocksOpen = pyqtSignal(int)
    signalHttpSocksStop = pyqtSignal()

    def __init__(self, *arg, **kwargs):
        super(IntranetProxyTab, self).__init__(*arg, **kwargs)
        self.setupUi(self)
        self.connectSignal()

    def connectSignal(self):
        self.btn_reverse.clicked.connect(self.reverseSocks)
        self.btn_bindHttp.clicked.connect(self.bindHttp)

    def reverseSocks(self):
        pass

    def bindHttp(self):
        if self.btn_bindHttp.isChecked():
            port = self.spinBox_bindHttpPort.value()
            self.textEdit_bindLog.append("【HTTP隧道方式】开始监听{}端口...".format(port))
            self.signalHttpSocksOpen.emit(port)
        else:
            self.textEdit_bindLog.append("【HTTP隧道方式】关闭监听...")
            self.signalHttpSocksStop.emit()
