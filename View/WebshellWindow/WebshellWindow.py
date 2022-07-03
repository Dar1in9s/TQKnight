from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from View.WebshellWindow.UI import Ui_WebshellWindow
from View.WebshellWindow import WebshellInfoTab, FileManageTab, TerminalTab, DatabaseTab, IntranetProxyTab, PluginTab
from View.qss import loadQSS


class WebshellWindow(QWidget, Ui_WebshellWindow):
    signalClose = pyqtSignal()
    signalRealClose = pyqtSignal(int)
    signalLoadPluginRequest = pyqtSignal()

    def __init__(self, webshell, proxy, *args, **kwargs):
        super(WebshellWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.webshell = webshell
        self.proxy = proxy

        self.webshellInfoTab = WebshellInfoTab()
        self.fileManageTab = FileManageTab()
        self.terminalTab = TerminalTab()
        self.databaseTab = DatabaseTab()
        self.intranetProxyTab = IntranetProxyTab()
        self.pluginTab = PluginTab()
        self.initUi()
        # self.setQSS()

    def initUi(self):
        self.layout_info.addWidget(self.webshellInfoTab)
        self.webshellInfoTab.initData({
            "url": self.webshell.url,
            "type": self.webshell.type,
            "time": self.webshell.time,
            "name": self.proxy.name
        })
        self.layout_file.addWidget(self.fileManageTab)
        self.layout_shell.addWidget(self.terminalTab)
        self.layout_database.addWidget(self.databaseTab)
        self.layout_IntranetProxy.addWidget(self.intranetProxyTab)
        self.layout_plugin.addWidget(self.pluginTab)
        self.tabWidget.currentChanged.connect(self.tabChanged)

    def setQSS(self):
        self.setStyleSheet(loadQSS("webshellWindow.qss"))

    def tabChanged(self):
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tab_plugin):
            self.signalLoadPluginRequest.emit()

    def getBaseInfoResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            self.webshellInfoTab.setBaseInfo(data)
            for drive in data["driveList"]:
                driveItem = QTreeWidgetItem()
                driveItem.setIcon(0, QIcon(":/file/drive.png"))
                driveItem.setText(0, drive)
                driveItem.setText(1, drive)
                self.fileManageTab.treeDirectory.addTopLevelItem(driveItem)

            if "linux" in data["os"].lower():
                self.fileManageTab.dirListInfo.tableWidget_file.setColumnCount(7)
                item = QTableWidgetItem()
                item.setText("所属用户")
                self.fileManageTab.dirListInfo.tableWidget_file.setHorizontalHeaderItem(5, item)
                item = QTableWidgetItem()
                item.setText("所属组")
                self.fileManageTab.dirListInfo.tableWidget_file.setHorizontalHeaderItem(6, item)

            self.terminalTab.start(data["user"], data["host"], data["currentPath"], data["os"])

    def closeEvent(self, evt):
        self.signalClose.emit()
        self.hide()
        evt.ignore()
