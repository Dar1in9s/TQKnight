from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from View import MainWindow
from Model import GroupModel, WebshellModel, ProxyModel, Proxy, Webshell
from Core import WebshellService
import sys
import copy
import pickle


class MainWindowController(QObject):
    signalProxyWindowShow = pyqtSignal()
    signalProxyWindowRefresh = pyqtSignal()
    signalWebshellConnect = pyqtSignal(Webshell)

    def __init__(self, *args, **kwargs):
        super(MainWindowController, self).__init__(*args, **kwargs)
        self.window = MainWindow()
        self.groupModel = GroupModel()
        self.webshellModel = WebshellModel()
        self.proxyModel = ProxyModel()
        self.webshellService = None
        if not self.groupModel.initTable() or not self.proxyModel.initTable():
            QMessageBox.critical(self.window, "警告", "数据库加载失败")
            sys.exit(1)
        self.connectSignal()
        self.refreshWebshellList()

    def connectSignal(self):
        self.window.webshellGroup.signalAddGroup.connect(self.addGroup)
        self.window.webshellGroup.signalDeleteGroup.connect(self.deleteGroup)
        self.window.webshellGroup.signalRenameGroup.connect(self.renameGroup)
        self.window.webshellGroup.signalRefreshWebshellList.connect(self.refreshWebshellList)
        self.window.webshellGroup.signalShowWebshellInfo.connect(self.showWebshellInfo)
        self.window.webshellGroup.signalShowUntitledWebshellInfo.connect(self.showUntitledWebshellInfo)
        self.window.webshellGroup.signalDeleteAllWebshellInGroup.connect(self.deleteAllWebshellInGroup)
        self.window.webshellGroup.signalDeleteWebshell.connect(self.deleteWebshell)
        self.window.webshellInfo.signalUpdate.connect(self.updateWebshellInfo)
        self.window.webshellInfo.signalAdd.connect(self.addWebshellInfo)
        self.window.webshellInfo.signalRefresh.connect(self.showWebshellInfo)
        self.window.webshellInfo.signalTest.connect(self.webshellTest)
        self.window.webshellInfo.signalConnect.connect(self.signalWebshellConnect.emit)
        self.window.signalProxyWindowShow.connect(self.signalProxyWindowShow.emit)
        self.window.signalProxyWindowRefresh.connect(self.signalProxyWindowRefresh.emit)
        self.window.signalExportData.connect(self.exportData)
        self.window.signalImportData.connect(self.importData)

    def refreshWebshellList(self):
        self.window.webshellGroup.showWebshellItem(self.groupModel.getGroup(), self.webshellModel.getWebshell())

    def showWebshellInfo(self, url):
        webshellObj = self.webshellModel.getWebshell({"url": url})[0]
        proxyObjs = self.proxyModel.getProxy()
        self.window.webshellInfo.showWebshellInfo(webshellObj, proxyObjs)

    def showUntitledWebshellInfo(self):
        proxyObjs = self.proxyModel.getProxy()
        self.window.webshellInfo.showWebshellInfo(self.window.webshellGroup.untitledWebshellObj, proxyObjs)

    def addGroup(self, groupName):
        result = {
            "status": "ok",
            "message": "",
            "groupName": groupName
        }
        if self.groupModel.isExist(groupName):
            result["status"] = "error"
            result["message"] = "该组已存在"
        elif self.webshellModel.getWebshell({"url": groupName}):
            result["status"] = "error"
            result["message"] = "组名不能和url相同"
        elif self.groupModel.addGroup(groupName):
            result["groupId"] = self.groupModel.getGroup({"name": groupName})[0].id
        else:
            result["status"] = "error"
            result["message"] = "添加失败"
        self.window.webshellGroup.addGroupResult(result)

    def deleteGroup(self, groupName):
        result = {
            "status": "ok",
            "message": "",
        }
        groupObj = self.groupModel.getGroup({"name": groupName})[0]
        where = {"groupId": groupObj.id}
        new = {"groupId": 1}
        if not self.groupModel.deleteGroup(groupName) or not self.webshellModel.modifyWebshell(new, where):
            result["status"] = "error"
            result["message"] = "删除失败"
        self.window.webshellGroup.deleteGroupResult(result)

    def renameGroup(self, oldGroupName, newGroupName):
        result = {
            "status": "ok",
            "message": "",
            "oldGroupName": oldGroupName
        }
        if self.groupModel.isExist(newGroupName):
            result["status"] = "error"
            result["message"] = "该组已存在"
        elif not self.groupModel.renameGroup(oldGroupName, newGroupName):
            result["status"] = "error"
            result["message"] = "改名失败"
        self.window.webshellGroup.renameGroupResult(result)

    def deleteAllWebshellInGroup(self, groupId):
        result = {
            "status": "ok",
            "message": "",
        }
        if not self.webshellModel.deleteWebshell({"groupId": groupId}):
            result["status"] = "error"
            result["message"] = "删除错误"
        self.window.webshellGroup.actionDeleteAllWebshellResult(result)

    def deleteWebshell(self, url):
        result = {
            "status": "ok",
            "message": "",
        }
        if not self.webshellModel.deleteWebshell({"url": url}):
            result["status"] = "error"
            result["message"] = "删除失败"
        self.window.webshellGroup.actionDeleteWebshellResult(result)

    def updateWebshellInfo(self, webshellObj):
        new = {
            "url": webshellObj.url,
            "passwd": webshellObj.passwd,
            "proxyId": webshellObj.proxyId,
            "type": webshellObj.type,
            "httpHeader": webshellObj.httpHeader,
            "note": webshellObj.note
        }
        where = {"id": webshellObj.id}
        result = {
            "status": "ok",
            "message": "",
        }
        if not self.webshellModel.modifyWebshell(new, where):
            result["status"] = "error"
            result["message"] = "保存出错"
        else:
            self.window.webshellGroup.tree_main.currentItem().setText(0, webshellObj.url)
            self.window.webshellGroup.tree_main.currentItem().setText(1, str(webshellObj.id))
            result["webshellObj"] = webshellObj
        self.window.webshellInfo.WebshellSaveResult(result)

    def addWebshellInfo(self, webshellObj):
        result = {
            "status": "ok",
            "message": "",
        }
        webshellObjResult = copy.deepcopy(webshellObj)
        if self.webshellModel.isExist(webshellObj.url):
            result["status"] = "error"
            result["message"] = "url已存在"
        elif not self.webshellModel.addWebshell(webshellObj):
            result["status"] = "error"
            result["message"] = "保存出错"
        else:
            self.window.webshellGroup.tree_main.currentItem().setText(0, webshellObjResult.url)
            self.window.webshellGroup.tree_main.currentItem().setText(1, str(webshellObjResult.id))
            result["webshellObj"] = webshellObjResult
            self.window.webshellGroup.untitledWebshellObj = Webshell()
        self.window.webshellInfo.WebshellSaveResult(result)

    def refreshProxy(self, deleteFlag):
        proxies = self.proxyModel.getProxy()
        self.window.webshellInfo.refreshProxy(proxies, deleteFlag)

    def exportData(self, fileName):
        result = {
            "status": "ok",
            "message": "",
        }
        try:
            data = {
                "group": self.groupModel.getGroup(),
                "proxy": self.proxyModel.getProxy(),
                "webshell": self.webshellModel.getWebshell()
            }
            with open(fileName, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            result["status"] = "error"
            result["message"] = "保存错误：" + str(e)
        self.window.exportResult(result)

    def importData(self, fileName):
        result = {
            "status": "ok",
            "message": "",
        }
        try:
            with open(fileName, "rb") as f:
                data = pickle.load(f)
            groups, proxies, webshell = data["group"], data["proxy"], data["webshell"]

            for g in groups:
                if not self.groupModel.isExist(g.name):
                    self.groupModel.addGroup(g.name)
                gid = self.groupModel.getGroup({"name": g.name})[0].id
                for w in webshell:
                    if w.groupId == g.id:
                        w.groupId = gid
            for p in proxies:
                proxyAdd = Proxy()
                proxyAdd.setValueByProxy(p)
                pidOld = p.id
                proxy = self.proxyModel.getProxy({"name": p.name})
                if not proxy:
                    pidNew = self.proxyModel.addProxy(proxyAdd)
                elif not p.eq(proxy[0]):
                    p.name = p.name + "_导入"
                    pidNew = self.proxyModel.addProxy(proxyAdd)
                else:
                    pidNew = proxy[0].id
                for w in webshell:
                    if w.proxyId == pidOld:
                        w.proxyId = pidNew
            for w in webshell:
                webshellAdd = Webshell()
                webshellAdd.setValueByWebshell(w)
                if not self.webshellModel.isExist(w.url):
                    self.webshellModel.addWebshell(webshellAdd)
                elif not w.eq(self.webshellModel.getWebshell({"url": w.url})[0]):
                    webshellAdd.url = w.url + "#导入"
                    self.webshellModel.addWebshell(webshellAdd)
        except Exception as e:
            result["status"] = "error"
            result["message"] = "导入错误：" + str(e)
        self.window.importDataResult(result)

    def webshellTest(self, url):
        webshellObj = self.webshellModel.getWebshell({"url": url})[0]
        proxy = self.proxyModel.getProxy({"id": webshellObj.proxyId})[0]
        self.webshellService = WebshellService(webshellObj, proxy)
        self.webshellService.signalShackHandResult.connect(self.webshellTestResult)
        self.webshellService.shackHand()

    def webshellTestResult(self, result):
        if result["status"]:
            message = "连接成功"
        else:
            message = "连接失败 " + result["message"]
        self.window.webshellInfo.webshellTestResult(message)

    def show(self):
        self.window.show()
        self.window.activateWindow()
