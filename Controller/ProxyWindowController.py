from PyQt5.QtCore import QObject, pyqtSignal
from View import ProxyWindow
from Model import WebshellModel, ProxyModel
import copy


class ProxyWindowController(QObject):
    signalProxyUpdate = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(ProxyWindowController, self).__init__(*args, **kwargs)
        self.proxyWindow = ProxyWindow()
        self.proxyModel = ProxyModel()
        self.webshellModel = WebshellModel()
        self.showProxies()
        self.connectSignal()

    def connectSignal(self):
        self.proxyWindow.signalAddProxy.connect(self.addProxy)
        self.proxyWindow.signalModifyProxy.connect(self.modifyProxy)
        self.proxyWindow.signalDeleteProxy.connect(self.deleteProxy)

    def showProxies(self):
        proxies = self.proxyModel.getProxy()
        self.proxyWindow.showProxies(proxies)

    def refresh(self):
        self.proxyWindow.tableWidget_proxy.setRowCount(0)
        self.showProxies()

    def addProxy(self, proxyObj):
        result = {
            "status": "ok",
            "message": "",
        }
        name = proxyObj.name
        if self.proxyModel.isExist(name):
            result["status"] = "error"
            result["message"] = "当前名字已存在"
        elif not self.proxyModel.addProxy(proxyObj):
            result["status"] = "error"
            result["message"] = "添加错误"
        else:
            self.signalProxyUpdate.emit(False)
        result["proxyObj"] = self.proxyModel.getProxy({"name": name})
        self.proxyWindow.addProxyResult(result)

    def modifyProxy(self, proxyObj):
        result = {
            "status": "ok",
            "message": "",
            "proxyObj": copy.deepcopy(proxyObj)
        }
        new = {
            "name": proxyObj.name,
            "protocol": proxyObj.protocol,
            "server": proxyObj.server,
            "port": proxyObj.port,
            "user": proxyObj.user,
            "passwd": proxyObj.passwd
        }
        proxyOld = self.proxyModel.getProxy({"id": proxyObj.id})[0]
        if proxyOld.eq(proxyObj):
            result["status"] = "noModify"
        elif proxyOld.name != proxyObj.name and self.proxyModel.isExist(proxyObj.name):
            result["status"] = "error"
            result["message"] = "该名字已存在"
        elif not self.proxyModel.modifyProxy(new, {"id": proxyObj.id}):
            result["status"] = "error"
            result["message"] = "修改错误"
        else:
            self.signalProxyUpdate.emit(False)
        self.proxyWindow.modifyProxyResult(result)

    def deleteProxy(self, dId):
        result = {
            "status": "ok",
            "message": "",
            "dId": dId
        }
        new = {"proxyId": 0}
        where = {"proxyId": dId}
        if not self.proxyModel.deleteProxy(dId) or not self.webshellModel.modifyWebshell(new, where):
            result["status"] = "error"
            result["message"] = "删除错误"
        else:
            self.signalProxyUpdate.emit(True)
        self.proxyWindow.deleteProxyResult(result)

    def show(self):
        self.proxyWindow.show()

