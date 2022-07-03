from Model.SQLModelObject import Group, SQL


class GroupModel:
    def initTable(self):
        if not self.isExist("default") and not self.addGroup("default"):
            return False
        return True

    def getGroup(self, where=None):
        return SQL.select(Group, where)

    def addGroup(self, groupName):
        return SQL.insert(Group(name=groupName))

    def deleteGroup(self, groupName):
        where = {"name": groupName}
        return SQL.delete(Group, where)

    def renameGroup(self, oldGroupName, newGroupName):
        where = {"name": oldGroupName}
        new = {"name": newGroupName}
        return SQL.update(Group, new, where)

    def isExist(self, groupName):
        where = {"name": groupName}
        if SQL.select(Group, where):
            return True
        return False
