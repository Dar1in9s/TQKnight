from PyQt5.QtWidgets import QMessageBox, QSplitter, QTreeWidget, QWidget, QTreeWidgetItem, QTableWidgetItem, \
    QTableWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QFile, QIODevice, QFileInfo
from PyQt5 import Qsci
from PyQt5.QtGui import QIntValidator, QIcon
from View.WebshellWindow.UI import Ui_DatabaseTab, Ui_DatabaseResultInfo, Ui_SqlEdit
import os


class DatabaseTab(Ui_DatabaseTab, QWidget):
    signalConnectDatabase = pyqtSignal(dict)
    signalShowTables = pyqtSignal(dict)
    signalSelectTableAttr = pyqtSignal(dict)
    signalSelectTableData = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(DatabaseTab, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.treeDatabase = QTreeWidget()
        self.databaseInfoResult = DatabaseInfoResult()
        self.splitter = QSplitter()
        self.sqlExecuteWindow = SQLExecWidget()
        self.initUi()
        self.connectSignal()

    def initUi(self):
        self.splitter.addWidget(self.treeDatabase)
        self.splitter.addWidget(self.databaseInfoResult)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setChildrenCollapsible(False)
        self.layout_main.addWidget(self.splitter)

        self.lineEdit_port.setValidator(QIntValidator())
        self.treeDatabase.setHeaderHidden(True)

    def connectSignal(self):
        self.btn_connect.clicked.connect(self.connectDatabase)
        self.btn_sql.clicked.connect(self.SqlExecuteWindowShow)
        self.treeDatabase.currentItemChanged.connect(self.treeItemChanged)

    def getConnParm(self):
        type_ = self.comboBox_type.currentText().strip()
        host = self.lineEdit_host.text().strip()
        port = self.lineEdit_port.text().strip()
        database = self.lineEdit_database.text().strip()
        user = self.lineEdit_user.text().strip()
        passwd = self.lineEdit_passwd.text().strip()
        parm = {}
        if type_ == "mysql":
            if not host:
                QMessageBox.warning(self, "提示", "服务器地址不能为空")
                return None
            if not user:
                QMessageBox.warning(self, "提示", "用户名不能为空")
                return None
            parm["host"] = host
            parm["port"] = port
            parm["database"] = database
            parm["user"] = user
            parm["passwd"] = passwd
        return parm

    def connectDatabase(self):
        self.treeDatabase.clear()
        self.databaseInfoResult.tableWidget_data.clear()
        self.databaseInfoResult.tableWidget_data.setRowCount(0)
        self.databaseInfoResult.tableWidget_attr.clear()
        self.databaseInfoResult.tableWidget_attr.setRowCount(0)
        parm = self.getConnParm()
        if parm:
            self.signalConnectDatabase.emit(parm)

    def connectDatabaseResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                self.treeDatabase.clear()
                data = result["data"]["data"]
                data.pop(0)
                for database in data:
                    dbItem = QTreeWidgetItem()
                    dbItem.setIcon(0, QIcon(":/database/database.png"))
                    dbItem.setText(0, database[0])
                    dbItem.setText(1, database[0])
                    self.treeDatabase.addTopLevelItem(dbItem)
            else:
                QMessageBox.warning(self, "提示", result['data']["msg"])

    def treeItemChanged(self):
        currentItem = self.treeDatabase.currentItem()
        if currentItem:
            parm = self.getConnParm()
            if parm:
                parm["current"] = currentItem.text(1)
                if not currentItem.parent():    # 数据库
                    self.signalShowTables.emit(parm)
                else:                           # 表
                    self.signalSelectTableAttr.emit(parm)

    def showTablesResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                data = result["data"]["data"]
                data.pop(0)
                currentItem = self.treeDatabase.currentItem()
                if not currentItem.parent() and currentItem.text(1) == result["data"]["current"]:
                    currentItem.takeChildren()
                    for table in data:
                        tbItem = QTreeWidgetItem(currentItem)
                        tbItem.setIcon(0, QIcon(":/database/table.png"))
                        tbItem.setText(0, table[0])
                        tbItem.setText(1, "{}.{}".format(result["data"]["current"], table[0]))
                    currentItem.setExpanded(True)

            else:
                QMessageBox.warning(self, "提示", result['data']["msg"])

    def selectTableAttrResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                data = result["data"]["data"]
                currentItem = self.treeDatabase.currentItem()
                if currentItem.parent() and currentItem.text(1) == result["data"]["current"]:
                    self.setResultDataInTable(data, self.databaseInfoResult.tableWidget_attr)
                    parm = self.getConnParm()
                    if parm:
                        parm["current"] = result["data"]["current"]
                        self.signalSelectTableData.emit(parm)
            else:
                QMessageBox.warning(self, "提示", result['data']["msg"])

    def selectTableDataResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                data = result["data"]["data"]
                currentItem = self.treeDatabase.currentItem()
                if currentItem.parent() and currentItem.text(1) == result["data"]["current"]:
                    self.setResultDataInTable(data, self.databaseInfoResult.tableWidget_data)
            else:
                QMessageBox.warning(self, "提示", result['data']["msg"])

    def SqlExecuteWindowShow(self):
        parm = self.getConnParm()
        if parm:
            parm["current"] = ""
            self.sqlExecuteWindow.init(parm)
            self.sqlExecuteWindow.show()

    @staticmethod
    def setResultDataInTable(data, table):
        table.setRowCount(0)
        table.horizontalHeader().setVisible(False)
        if not data:
            return
        headerLabels = data.pop(0)
        table.setRowCount(0)
        table.setColumnCount(len(headerLabels))
        table.setHorizontalHeaderLabels(headerLabels)
        table.horizontalHeader().setVisible(True)
        for dataRow in data:
            row = table.rowCount()
            table.insertRow(row)
            for i in range(len(dataRow)):
                table.setItem(row, i, QTableWidgetItem(dataRow[i]))


class SQLExecWidget(QWidget):
    signalExecuteSQL = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(SQLExecWidget, self).__init__(*args, **kwargs)
        self.layout_ = QHBoxLayout(self)
        self.spliter = QSplitter(Qt.Vertical)
        self.sqlEditor = SQLEdit()
        self.tableResult = QTableWidget()
        self.connParm = None
        self.initUi()
        self.connectSignal()

    def initUi(self):
        self.spliter.addWidget(self.sqlEditor)
        self.spliter.addWidget(self.tableResult)
        self.spliter.setStretchFactor(0, 4)
        self.spliter.setStretchFactor(1, 6)
        self.layout_.addWidget(self.spliter)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.resize(1000, 600)
        self.setWindowTitle("自定义SQL执行")

    def connectSignal(self):
        self.sqlEditor.btn_execute.clicked.connect(self.executeSQL)
        self.sqlEditor.btn_clear.clicked.connect(lambda: self.sqlEditor.editor.clear())
        self.sqlEditor.btn_save.clicked.connect(self.saveResultOfSQL)

    def init(self, connParm):
        self.sqlEditor.editor.clear()
        self.tableResult.horizontalHeader().setVisible(False)
        self.tableResult.setRowCount(0)
        self.connParm = connParm
        self.sqlEditor.editor.setText("show databases;")

    def executeSQL(self):
        sql = self.sqlEditor.editor.text().strip()
        if self.connParm and sql:
            self.connParm["sql"] = sql
            self.signalExecuteSQL.emit(self.connParm)

    def executeSQLResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                data = result["data"]["data"]
                DatabaseTab.setResultDataInTable(data, self.tableResult)
            else:
                QMessageBox.warning(self, "提示", result['data']["msg"])

    def saveResultOfSQL(self):
        fileName, ok = QFileDialog.getSaveFileName(self, "保存结果到文件", "download/", "file(*.csv)")
        if not ok:
            return
        if QFile.exists(fileName):
            QFile.remove(fileName)
        saveFile = QFile(fileName)
        if not saveFile.open(QIODevice.WriteOnly):
            return QMessageBox.warning(self, "提示", "保存文件失败")
        header = []
        for i in range(self.tableResult.columnCount()):
            header.append(self.tableResult.horizontalHeaderItem(i).text())
        saveFile.write((",".join(header) + "\n").encode(errors="ignore"))
        for i in range(self.tableResult.rowCount()):
            data = []
            for j in range(self.tableResult.columnCount()):
                data.append(self.tableResult.item(i, j).text())
            saveFile.write((",".join(data) + "\n").encode(errors="ignore"))
        QMessageBox.information(self, "提示", "保存完成")
        os.startfile(QFileInfo(saveFile).path())


class DatabaseInfoResult(Ui_DatabaseResultInfo, QWidget):
    def __init__(self, *args, **kwargs):
        super(DatabaseInfoResult, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(400, 400)


class SQLEdit(Ui_SqlEdit, QWidget):
    def __init__(self, *args, **kwargs):
        super(SQLEdit, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.editor = Qsci.QsciScintilla()
        self.layout_Editor.addWidget(self.editor)
        self.editor.setLexer(Qsci.QsciLexerSQL())
