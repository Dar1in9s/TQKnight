from Model.SQLModelObject import Proxy, sessionMaker, SQL


class ProxyModel:
    def __init__(self):
        self.session = sessionMaker()
        self.tableName = "proxy"

    def initTable(self):
        if not self.isExist("不使用代理") and not self.addProxy(Proxy(name="不使用代理", id=0)):
            return False
        return True

    def addProxy(self, proxyObj):
        return SQL.insert(proxyObj)

    def getProxy(self, where=None):
        return SQL.select(Proxy, where)

    def modifyProxy(self, new, where):
        return SQL.update(Proxy, new, where)

    def deleteProxy(self, dId):
        return SQL.delete(Proxy, {"id": dId})

    def isExist(self, proxyName):
        if SQL.select(Proxy, {"name": proxyName}):
            return True
        return False

