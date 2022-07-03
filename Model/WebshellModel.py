from Model.SQLModelObject import Webshell, SQL


class WebshellModel:
    def getWebshell(self, where=None):
        return SQL.select(Webshell, where)

    def modifyWebshell(self, new, where):
        return SQL.update(Webshell, new, where)

    def addWebshell(self, webshellObj):
        return SQL.insert(webshellObj)

    def deleteWebshell(self, where):
        return SQL.delete(Webshell, where)

    def isExist(self, url):
        where = {"url": url}
        if SQL.select(Webshell, where):
            return True
        return False
