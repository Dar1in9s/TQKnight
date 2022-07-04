from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from Controller import MainWindowController, ProxyWindowController, WebshellWindowController
import View.qrc.img_rc
import sys


class MainController(QObject):
    def __init__(self, *args, **kwargs):
        super(MainController, self).__init__(*args, **kwargs)
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon(":/other/logo.png"))
        self.mainWindowController = MainWindowController()
        self.proxyWindowController = ProxyWindowController()
        self.webshellWindowControllerList = {}
        self.connectSignal()

    def connectSignal(self):
        self.mainWindowController.window.signalClose.connect(self.mainWindowClose)
        self.mainWindowController.signalProxyWindowShow.connect(self.proxyWindowController.show)
        self.mainWindowController.signalWebshellConnect.connect(self.showWebshellWindow)
        self.mainWindowController.signalProxyWindowRefresh.connect(self.proxyWindowController.refresh)
        self.proxyWindowController.signalProxyUpdate.connect(self.mainWindowController.refreshProxy)

    def showWebshellWindow(self, webshell):
        if webshell.id not in self.webshellWindowControllerList.keys():
            proxy = self.proxyWindowController.proxyModel.getProxy({"id": webshell.proxyId})[0]
            webshellWindowController = WebshellWindowController(webshell, proxy)
            webshellWindowController.webshellWindow.signalRealClose.connect(self.closeWebshellWindowController)

            self.webshellWindowControllerList[webshell.id] = webshellWindowController
            webshellWindowController.show()
        else:
            self.webshellWindowControllerList[webshell.id].show()

    def closeWebshellWindowController(self, shellId):
        self.webshellWindowControllerList.pop(shellId)
        self.mainWindowController.show()

    def mainWindowClose(self):
        if self.webshellWindowControllerList:
            self.mainWindowController.window.hide()
        else:
            self.mainWindowController.window.deleteLater()

    def run(self):
        self.mainWindowController.show()
        return self.app.exec_()
