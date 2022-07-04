from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QWidget, QInputDialog, QMessageBox, QTableWidgetItem, \
    QAbstractItemView, QMenu, QAction, QLineEdit, QFileDialog, QSplitter, QVBoxLayout, QShortcut, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor, QIcon, QKeySequence, QFontDatabase
import json
import validators
from Model.SQLModelObject import Webshell
from View.MainWindow.UI import Ui_MainWindow, Ui_WebshellInfo, Ui_webshellGroup
from View.ProxyWindow.ProxyWindow import ProxyWindow
from View.qss import loadQSS


class MainWindow(QMainWindow, Ui_MainWindow):
    signalClose = pyqtSignal()
    signalProxyWindowShow = pyqtSignal()
    signalProxyWindowRefresh = pyqtSignal()
    signalExportData = pyqtSignal(str)
    signalImportData = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.spliter = QSplitter()
        self.webshellInfoContainer = QWidget()
        self.layoutWebshellInfoContainer = QVBoxLayout(self.webshellInfoContainer)

        self.webshellInfo = WebshellInfo()
        self.webshellGroup = WebshellGroup(self.webshellInfo)
        self.proxyWindow = ProxyWindow()

        self.initUi()
        self.connectSignal()
        # self.setQSS()
        # QShortcut(QKeySequence("Ctrl+W"), self, self.setQSS)

    def initUi(self):
        self.layoutWebshellInfoContainer.setContentsMargins(0, 0, 0, 0)
        self.layoutWebshellInfoContainer.addWidget(self.webshellInfo)
        self.webshellInfoContainer.setMinimumWidth(890)

        self.spliter.addWidget(self.webshellGroup)
        self.spliter.addWidget(self.webshellInfoContainer)
        self.spliter.setStretchFactor(0, 3)
        self.spliter.setStretchFactor(1, 7)
        self.spliter.setChildrenCollapsible(False)

        self.layout_main.addWidget(self.spliter)
        self.webshellInfo.hide()
        self.proxyWindow.hide()

    def connectSignal(self):
        self.action_proxy.triggered.connect(self.menuActionProxy)
        self.action_export.triggered.connect(self.actionExportClicked)
        self.action_import.triggered.connect(self.actionImportClicked)

    def setQSS(self):
        # 左边
        self.webshellGroup.btn_renamegroup.setObjectName("group")
        self.webshellGroup.btn_deletegroup.setObjectName("group")
        self.webshellGroup.btn_addgroup.setObjectName("group")
        self.webshellGroup.tree_main.setObjectName("webshell")
        # 右边
        self.webshellInfo.widget_btn.setObjectName("operateBtn")

        self.webshellInfo.btn_webshelltest.setObjectName("operate")
        self.webshellInfo.btn_webshellconnect.setObjectName("operate")

        self.webshellInfo.comboBox_type.setView(QListView())
        self.webshellInfo.comboBox_type.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.webshellInfo.comboBox_type.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.webshellInfo.comboBox_proxy.setView(QListView())
        self.webshellInfo.comboBox_proxy.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.webshellInfo.comboBox_proxy.view().window().setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet(loadQSS("mainWindow.qss"))

    def menuActionProxy(self):
        self.signalProxyWindowShow.emit()

    def actionExportClicked(self):
        fileName, ok = QFileDialog.getSaveFileName(self, "保存到文件", "./", "file(*)")
        if fileName:
            self.signalExportData.emit(fileName)

    def exportResult(self, result):
        if result["status"] == "ok":
            QMessageBox.information(self, "提示", "保存成功")
        else:
            QMessageBox.warning(self, "注意", result["message"])

    def actionImportClicked(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "导入数据", "./", "file(*)")
        if fileName:
            self.signalImportData.emit(fileName)

    def importDataResult(self, result):
        if result["status"] == "ok":
            QMessageBox.information(self, "提示", "导入成功")
            self.webshellGroup.signalRefreshWebshellList.emit()
            self.signalProxyWindowRefresh.emit()
        else:
            QMessageBox.warning(self, "注意", result["message"])

    def closeEvent(self, event):
        self.signalClose.emit()
        event.ignore()


class WebshellGroup(QWidget, Ui_webshellGroup):
    signalAddGroup = pyqtSignal(str)
    signalDeleteGroup = pyqtSignal(str)
    signalRenameGroup = pyqtSignal(str, str)
    signalRefreshWebshellList = pyqtSignal()
    signalShowWebshellInfo = pyqtSignal(str)
    signalShowUntitledWebshellInfo = pyqtSignal()
    signalDeleteAllWebshellInGroup = pyqtSignal(int)
    signalDeleteWebshell = pyqtSignal(str)

    def __init__(self, webshellInfo, *args, **kwargs):
        super(WebshellGroup, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()
        self.webshellInfo = webshellInfo
        self.currentRenameItem = None
        self.untitledWebshellObj = Webshell()
        self.groupRenameInfo = {}
        self.connectSignal()

    def initUi(self):
        self.btn_deletegroup.setEnabled(False)
        self.btn_renamegroup.setEnabled(False)
        self.tree_main.setContextMenuPolicy(Qt.CustomContextMenu)

    def connectSignal(self):
        self.btn_addgroup.clicked.connect(self.btnAddGroupClicked)
        self.btn_deletegroup.clicked.connect(self.btnDeleteGroupClicked)
        self.btn_renamegroup.clicked.connect(self.btnRenameGroupClicked)
        self.tree_main.currentItemChanged.connect(self.currentItemChanged)
        self.tree_main.customContextMenuRequested.connect(self.showWebshellItemMenu)

    def btnAddGroupClicked(self):
        text, ok = QInputDialog.getText(self, '添加分组', '请输入分组名：')
        if ok and text.strip():
            self.signalAddGroup.emit(text.strip())

    def addGroupResult(self, result):
        if result["status"] == "error":
            QMessageBox.warning(self, "警告", result["message"])
        else:
            groupItem = QTreeWidgetItem()
            groupItem.setIcon(0, QIcon(":/webshell/group.png"))
            groupItem.setText(0, result["groupName"])
            groupItem.setText(1, str(result["groupId"]))
            self.tree_main.addTopLevelItem(groupItem)

    def btnDeleteGroupClicked(self):
        currentGroupItem = self.tree_main.currentItem()
        if not currentGroupItem:
            return
        if currentGroupItem.childCount():
            reply = QMessageBox.question(self, "提示", "删除后组内webshell将移至默认分组。\n确定删除吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        groupName = currentGroupItem.text(0)
        self.signalDeleteGroup.emit(groupName)

    def deleteGroupResult(self, result):
        if result["status"] == "error":
            QMessageBox.warning(self, "警告", result["message"])
        self.signalRefreshWebshellList.emit()

    def btnRenameGroupClicked(self):
        currentGroupItem = self.tree_main.currentItem()
        if not currentGroupItem:
            return
        lineEdit = QLineEdit(currentGroupItem.text(0), self)
        lineEdit.setFocus()
        lineEdit.selectAll()
        lineEdit.editingFinished.connect(self.renameGroupFinished)
        self.groupRenameInfo["lineEdit"] = lineEdit
        self.groupRenameInfo["item"] = currentGroupItem
        self.tree_main.setItemWidget(currentGroupItem, 0, lineEdit)

    def renameGroupResult(self, result):
        if result["status"] == "error":
            QMessageBox.warning(self, "警告", result["message"])
            self.currentRenameItem.setText(0, result["oldGroupName"])

    def renameGroupFinished(self):
        item = self.groupRenameInfo["item"]
        lineEdit = self.tree_main.itemWidget(item, 0)
        oldGroupName = item.text(0)
        newGroupName = lineEdit.text()

        item.setText(0, newGroupName)
        self.tree_main.removeItemWidget(item, 0)
        lineEdit.destroy()
        if oldGroupName.strip() != newGroupName.strip():
            self.signalRenameGroup.emit(oldGroupName, newGroupName)
        self.groupRenameInfo.clear()

    def currentItemChanged(self):
        if self.groupRenameInfo:
            self.renameGroupFinished()
        currentItem = self.tree_main.currentItem()
        # 没有父节点，即分组
        if currentItem and not currentItem.parent():
            currentItem.setExpanded(True)
            self.webshellInfo.hide()
            if currentItem.text(0) != "default":
                self.btn_deletegroup.setEnabled(True)
                self.btn_renamegroup.setEnabled(True)
            else:
                self.btn_deletegroup.setEnabled(False)
                self.btn_renamegroup.setEnabled(False)
        # 有父节点，即webshell
        elif currentItem:
            self.btn_deletegroup.setEnabled(False)
            self.btn_renamegroup.setEnabled(False)
            url = currentItem.text(0)
            if url == "untitled":
                self.untitledWebshellObj.groupId = int(self.tree_main.currentItem().parent().text(1))
                self.signalShowUntitledWebshellInfo.emit()
            else:
                self.signalShowWebshellInfo.emit(url)

    def showWebshellItem(self, groupObjs, webshellObjs):
        self.tree_main.clear()
        # 显示组
        groups = {}
        for groupObj in groupObjs:
            groups[groupObj.id] = groupObj.name
            groupItem = QTreeWidgetItem()
            groupItem.setIcon(0, QIcon(":/webshell/group.png"))
            groupItem.setText(0, groupObj.name)
            groupItem.setText(1, str(groupObj.id))
            self.tree_main.addTopLevelItem(groupItem)
        # 显示webshell
        for webshellObj in webshellObjs:
            groupName = groups[webshellObj.groupId]
            groupItem = self.tree_main.findItems(groupName, Qt.MatchExactly, 0)[0]
            item = QTreeWidgetItem(groupItem)
            item.setIcon(0, QIcon(":/webshell/webshell.png"))
            item.setText(0, webshellObj.url)
        self.tree_main.findItems("default", Qt.MatchExactly, 0)[0].setExpanded(True)

    def showWebshellItemMenu(self):
        currentItem = self.tree_main.currentItem()
        if not currentItem:
            return
        menu = QMenu(self)
        menu.setObjectName("webshell")
        # 分组
        if not currentItem.parent():
            actionAddWebshell = QAction("添加webshell", self)
            actionAddWebshell.triggered.connect(self.actionAddWebshellClicked)
            actionDeleteAllWebshell = QAction("删除该组所有webshell", self)
            actionDeleteAllWebshell.triggered.connect(self.actionDeleteAllWebshellClicked)

            actionAddGroup = QAction("添加分组", self)
            actionAddGroup.triggered.connect(self.btnAddGroupClicked)
            actionDeleteGroup = QAction("删除分组", self)
            actionDeleteGroup.triggered.connect(self.btnDeleteGroupClicked)
            actionRenameGroup = QAction("重命名分组", self)
            actionRenameGroup.triggered.connect(self.btnRenameGroupClicked)
            if currentItem.text(0) == "default":
                actionDeleteGroup.setEnabled(False)
                actionRenameGroup.setEnabled(False)
            if not currentItem.childCount():
                actionDeleteAllWebshell.setEnabled(False)
            menu.addAction(actionAddWebshell)
            menu.addAction(actionDeleteAllWebshell)
            menu.addSeparator()
            menu.addAction(actionAddGroup)
            menu.addAction(actionRenameGroup)
            menu.addAction(actionDeleteGroup)
        # webshell
        elif currentItem.parent():
            actionDeleteWebshell = QAction("删除webshell", self)
            actionDeleteWebshell.triggered.connect(self.actionDeleteWebshellClicked)
            actionAddGroup = QAction("添加分组", self)
            actionAddGroup.triggered.connect(self.btnAddGroupClicked)

            menu.addAction(actionDeleteWebshell)
            menu.addSeparator()
            menu.addAction(actionAddGroup)
        menu.exec_(QCursor.pos())

    def actionAddWebshellClicked(self):
        groupItem = self.tree_main.currentItem()
        item = QTreeWidgetItem(groupItem)
        item.setText(0, "untitled")
        item.setIcon(0, QIcon(":/webshell/webshell.png"))
        self.tree_main.setCurrentItem(item)

    def actionDeleteAllWebshellClicked(self):
        groupId = int(self.tree_main.currentItem().text(1))
        self.signalDeleteAllWebshellInGroup.emit(groupId)

    def actionDeleteAllWebshellResult(self, result):
        if result["status"] == "error":
            return QMessageBox.warning(self, "提示", result["message"])
        currentItem = self.tree_main.currentItem()
        for i in range(currentItem.childCount()):
            currentItem.removeChild(currentItem.child(0))

    def actionDeleteWebshellClicked(self):
        currentItem = self.tree_main.currentItem()
        url = currentItem.text(0)
        if url == "untitled":
            currentItem.parent().removeChild(currentItem)
        else:
            self.signalDeleteWebshell.emit(url)

    def actionDeleteWebshellResult(self, result):
        if result["status"] == "error":
            return QMessageBox.warning(self, "注意", result["message"])
        currentItem = self.tree_main.currentItem()
        currentItem.parent().removeChild(currentItem)


class WebshellInfo(QWidget, Ui_WebshellInfo):
    signalUpdate = pyqtSignal(Webshell)
    signalAdd = pyqtSignal(Webshell)
    signalRefresh = pyqtSignal(str)
    signalTest = pyqtSignal(str)
    signalConnect = pyqtSignal(Webshell)

    def __init__(self, *args, **kwargs):
        super(WebshellInfo, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()
        self.connectSignal()

    def initUi(self):
        self.tableWidget_httpheader.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_httpheader.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tableWidget_httpheader.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_httpheader.setColumnCount(2)
        self.tableWidget_httpheader.verticalHeader().setVisible(False)
        self.tableWidget_httpheader.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_httpheader.setHorizontalHeaderLabels(["name", "value"])
        self.tableWidget_httpheader.setColumnWidth(0, 200)
        self.tableWidget_httpheader.setFocusPolicy(Qt.NoFocus)

    def connectSignal(self):
        self.btn_httpheader_add.clicked.connect(self.btnHttpheaderAddClicked)
        self.btn_httpheader_delete.clicked.connect(self.btnHttpheaderDeleteClicked)
        self.btn_webshellsave.clicked.connect(self.btnWebshellSaveClicked)
        self.btn_webshellrefresh.clicked.connect(self.btnWebshellRefreshClicked)
        self.btn_webshelltest.clicked.connect(self.btnWebshellTestClicked)
        self.btn_webshellconnect.clicked.connect(self.btnWebshellConnectClicked)

    def btnHttpheaderAddClicked(self):
        row = self.tableWidget_httpheader.rowCount()
        self.tableWidget_httpheader.insertRow(row)
        self.tableWidget_httpheader.setItem(row, 0, QTableWidgetItem())
        self.tableWidget_httpheader.setItem(row, 1, QTableWidgetItem())
        # self.tableWidget_httpheader.resizeRowsToContents()

    def btnHttpheaderDeleteClicked(self):
        row = self.tableWidget_httpheader.currentIndex().row()
        self.tableWidget_httpheader.removeRow(row)

    def btnWebshellSaveClicked(self):
        # 处理http头
        headers = []
        removeNum = 0
        for i in range(self.tableWidget_httpheader.rowCount()):
            i = i - removeNum
            itemName = self.tableWidget_httpheader.item(i, 0)
            itemValue = self.tableWidget_httpheader.item(i, 1)
            name = itemName.text().strip()
            value = itemValue.text().strip()
            header = {"name": name, "value": value}
            if not name or not value or header in headers:
                self.tableWidget_httpheader.removeRow(itemName.row())
                removeNum += 1
            else:
                headers.append(header)

        # 检查url和密码
        url = self.lineEdit_url.text().strip()
        passwd = self.lineEdit_passwd.text().strip()
        if not url or not passwd:
            return QMessageBox.warning(self, "提示", "url或密码不能为空")
        if not validators.url(url):
            return QMessageBox.warning(self, "提示", "url格式不正确")

        webshellObj = self.property("webshellObj")
        webshellObj.url = url
        webshellObj.passwd = passwd
        webshellObj.time = self.lineEdit_time.text().strip()
        webshellObj.type = self.comboBox_type.currentText()
        webshellObj.proxyId = self.comboBox_proxy.currentIndex()
        webshellObj.note = self.textEdit_note.toPlainText().strip()
        webshellObj.httpHeader = json.dumps(headers)
        if not webshellObj.id:
            self.signalAdd.emit(webshellObj)
        else:
            self.signalUpdate.emit(webshellObj)

    def WebshellSaveResult(self, result):
        if result["status"] == "error":
            QMessageBox.warning(self, "提示", result["message"])
        else:
            self.setProperty("webshellObj", result["webshellObj"])
            QMessageBox.information(self, "提示", "保存成功")

    def btnWebshellRefreshClicked(self):
        if self.property("webshellObj").url:
            self.signalRefresh.emit(self.property("webshellObj").url)

    def btnWebshellTestClicked(self):
        webshellObj = self.property("webshellObj")
        if webshellObj.url and webshellObj.passwd:
            self.signalTest.emit(webshellObj.url)

    def webshellTestResult(self, message):
        QMessageBox.information(self, "提示", message)

    def btnWebshellConnectClicked(self):
        webshellObj = self.property("webshellObj")
        if webshellObj.url and webshellObj.passwd:
            self.signalConnect.emit(webshellObj)

    def showWebshellInfo(self, webshellObj, proxyObjs):
        self.setProperty("webshellObj", webshellObj)

        # self.comboBox_type.clear()
        # self.comboBox_type.addItem("PHP")
        self.comboBox_proxy.clear()
        for proxy in proxyObjs:
            self.comboBox_proxy.addItem(proxy.name)

        self.lineEdit_url.setText(webshellObj.url)
        self.lineEdit_time.setText(webshellObj.time)
        self.lineEdit_passwd.setText(webshellObj.passwd)
        self.textEdit_note.setText(webshellObj.note)
        self.comboBox_proxy.setCurrentIndex(webshellObj.proxyId)
        # self.comboBox_type.setCurrentText(webshellObj.type)

        self.tableWidget_httpheader.setRowCount(0)
        for header in json.loads(webshellObj.httpHeader):
            row = self.tableWidget_httpheader.rowCount()
            self.tableWidget_httpheader.insertRow(row)
            self.tableWidget_httpheader.setItem(row, 0, QTableWidgetItem(header["name"]))
            self.tableWidget_httpheader.setItem(row, 1, QTableWidgetItem(header["value"]))
            # self.tableWidget_httpheader.resizeRowsToContents()
        self.show()

    def refreshProxy(self, proxies, deleteFlag):
        if self.isVisible():
            self.comboBox_proxy.clear()
            for proxy in proxies:
                self.comboBox_proxy.addItem(proxy.name)
            if deleteFlag:
                self.property("webshellObj").proxyId = 0
            self.comboBox_proxy.setCurrentIndex(self.property("webshellObj").proxyId)
