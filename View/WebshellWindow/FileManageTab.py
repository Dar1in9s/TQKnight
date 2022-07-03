from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox, QSplitter, QTreeWidget, QHBoxLayout, \
    QTableWidgetItem, QMenu, QAction, QInputDialog, QFileDialog, QProgressDialog
from PyQt5 import Qsci
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QFileInfo
from View.WebshellWindow.UI import Ui_DirListInfo, Ui_OpenFileInfo
from binaryornot.check import is_binary_string
import base64
import time
import os


class FileManageTab(QWidget):
    signalListDirectory = pyqtSignal(str)
    signalOpenFile = pyqtSignal(str)
    signalUpdateFile = pyqtSignal(dict)
    signalOpenPath = pyqtSignal(str)
    signalNewFile = pyqtSignal(str)
    signalNewDir = pyqtSignal(str)
    signalDeleteFiles = pyqtSignal(list)
    signalModifyFileTime = pyqtSignal(dict)
    signalRenameFile = pyqtSignal(dict)
    signalDownloadFile = pyqtSignal(dict)
    signalDownloadFileCancel = pyqtSignal()
    signalUploadFile = pyqtSignal(dict)
    signalUploadFileCancel = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(FileManageTab, self).__init__(*args, **kwargs)
        self.layoutMain = QHBoxLayout(self)
        self.splitter = QSplitter()
        self.dirListInfo = DirListInfo()
        self.treeDirectory = QTreeWidget()

        self.openFileList = {}
        self.refreshFlag = False
        self.itemOld = None
        self.downloadProgressDialog = None
        self.uploadProgressDialog = None
        self.initUi()
        self.connectSignal()

    def connectSignal(self):
        self.treeDirectory.currentItemChanged.connect(self.listDirectory)
        self.dirListInfo.tableWidget_file.doubleClicked.connect(self.fileOpenDoubleClicked)
        self.dirListInfo.tableWidget_file.customContextMenuRequested.connect(self.dirListInfoMenu)
        self.dirListInfo.btn_pre.clicked.connect(self.backToPre)
        self.dirListInfo.btn_fileRefresh.clicked.connect(self.fileRefresh)
        self.dirListInfo.btn_fileOpen.clicked.connect(self.openPath)

    def initUi(self):
        self.layoutMain.addWidget(self.splitter)
        self.splitter.addWidget(self.treeDirectory)
        self.splitter.addWidget(self.dirListInfo)
        self.splitter.setChildrenCollapsible(False)
        self.treeDirectory.setHeaderHidden(True)

    def listDirectory(self, itemNow=None, itemOld=None):
        if itemNow and itemOld:
            self.itemOld = itemOld
        currentItem = self.treeDirectory.currentItem()
        if currentItem:
            path = currentItem.text(1)
            self.signalListDirectory.emit(path)

    def listDirectoryResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            currentItem = self.treeDirectory.currentItem()
            if data["status"]:
                if currentItem.text(1) == data["dir"]:
                    self.dirListInfo.lineEdit_filePath.setText(data["dir"])
                    self.dirListInfo.currentDirectory = data["dir"]
                    self.dirListInfo.tableWidget_file.setRowCount(0)
                    if self.refreshFlag:
                        currentItem.takeChildren()
                    changeDirFlag = True if currentItem.childCount() else False

                    for file in data["files"]:
                        if file["type"] == "dir" and (not changeDirFlag or self.refreshFlag):
                            item = QTreeWidgetItem(currentItem)
                            item.setIcon(0, QIcon(":/file/folder.png"))
                            item.setText(0, file["name"])
                            item.setText(1, data["dir"] + file["name"] + "/")

                        row = self.dirListInfo.tableWidget_file.rowCount()
                        self.dirListInfo.tableWidget_file.insertRow(row)
                        fileNameItem = QTableWidgetItem(file["name"])
                        fileType = "file" if file["type"] == "file" else "folder"
                        fileNameItem.setIcon(QIcon(":/file/{}.png".format(fileType)))
                        self.dirListInfo.tableWidget_file.setItem(row, 0, fileNameItem)
                        self.dirListInfo.tableWidget_file.setItem(row, 1, QTableWidgetItem(file["mtime"]))
                        self.dirListInfo.tableWidget_file.setItem(row, 2, QTableWidgetItem(file["type"]))
                        self.dirListInfo.tableWidget_file.setItem(row, 3, QTableWidgetItem(str(file["size"]) + "KB"))
                        self.dirListInfo.tableWidget_file.setItem(row, 4, QTableWidgetItem(file["perms"]))
                        if self.dirListInfo.tableWidget_file.columnCount() == 7:
                            self.dirListInfo.tableWidget_file.setItem(row, 5, QTableWidgetItem(file["user"]))
                            self.dirListInfo.tableWidget_file.setItem(row, 6, QTableWidgetItem(file["group"]))
                            self.dirListInfo.tableWidget_file.setColumnWidth(4, 100)
                            self.dirListInfo.tableWidget_file.setColumnWidth(5, 80)

                self.refreshFlag = False
                currentItem.setExpanded(True)
            else:
                QMessageBox.warning(self, "提示", "当前目录不存在或无权限")
                if self.itemOld:
                    self.treeDirectory.setCurrentItem(self.itemOld)
                    self.itemOld = None

    def fileOpenDoubleClicked(self):
        row = self.dirListInfo.tableWidget_file.currentRow()
        fileName = self.dirListInfo.tableWidget_file.item(row, 0).text()

        path = self.dirListInfo.currentDirectory + fileName
        type_ = self.dirListInfo.tableWidget_file.item(row, 2).text()
        if type_ == "dir":
            currentTreeItem = self.treeDirectory.currentItem()
            for i in range(currentTreeItem.childCount()):
                if currentTreeItem.child(i).text(0) == fileName:
                    self.treeDirectory.setCurrentItem(currentTreeItem.child(i))
                    break
        else:
            if path in self.openFileList.keys():
                self.openFileList[path].activateWindow()
            else:
                fileSize = int(self.dirListInfo.tableWidget_file.item(row, 3).text()[:-2])
                if fileSize > 1024:
                    return QMessageBox.warning(self, "提示", "文件大于1M，请下载到本地打开")
                self.signalOpenFile.emit(path)

    def openFileResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            if data["status"]:
                path = data["file"]
                contents = base64.b64decode(data["contents"].encode())
                if is_binary_string(contents[:1024]) or is_binary_string(contents[-1024:]):
                    return QMessageBox.warning(self, "提示", "当前文件为二进制文件，请下载后查看")
                contents = contents.decode()
                if path in self.openFileList.keys():  # refresh
                    self.openFileList[path].editor.setText(contents)
                    self.openFileList[path].editor.contents = contents
                    self.openFileList[path].activateWindow()
                else:
                    openFileInfo = OpenFileInfo(path, contents)
                    openFileInfo.signalClosed.connect(self.openFileList.pop)
                    openFileInfo.signalRefresh.connect(self.signalOpenFile.emit)
                    openFileInfo.signalSave.connect(self.signalUpdateFile.emit)
                    openFileInfo.show()
                    self.openFileList[path] = openFileInfo
            else:
                QMessageBox.warning(self, "提示", "当前文件不存在或无权限")

    def saveFileResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            path = data["file"]
            if data["status"]:
                self.openFileList[path].contents = self.openFileList[path].editor.text()
                QMessageBox.information(self.openFileList[path], "提示", "保存成功")
            else:
                QMessageBox.warning(self.openFileList[path], "提示", "保存失败")

    def backToPre(self):
        currentItem = self.treeDirectory.currentItem()
        if currentItem and currentItem.parent():
            self.treeDirectory.setCurrentItem(currentItem.parent())

    def fileRefresh(self):
        self.refreshFlag = True
        self.listDirectory()

    def openPath(self):
        path = self.dirListInfo.lineEdit_filePath.text().strip()
        path = QFileInfo(path).filePath()
        self.dirListInfo.lineEdit_filePath.setText(path)
        while "//" in path:
            path = path.replace("//", "/")
        if not path:
            return QMessageBox.warning(self, "提示", "路径不能为空")
        if self.dirListInfo.currentDirectory == path:
            self.dirListInfo.btn_fileRefresh.click()
        else:
            self.signalOpenPath.emit(path)

    def openPathResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            if data["status"]:
                path = data["path"]
                if data["type"] == "file":
                    if path in self.openFileList.keys():
                        self.openFileList[path].activateWindow()
                    else:
                        self.signalOpenFile.emit(path)
                else:
                    nodeItem = None
                    nodeList = path.split("/")
                    currentPath = nodeList.pop(0) + "/"
                    if nodeList and nodeList[-1] == "":
                        nodeList.pop(-1)

                    for i in range(self.treeDirectory.topLevelItemCount()):
                        item = self.treeDirectory.topLevelItem(i)
                        if item.text(0) == currentPath:
                            nodeItem = item
                            break

                    for node in nodeList:
                        currentPath = currentPath + node + "/"
                        for i in range(nodeItem.childCount()):
                            item = nodeItem.child(i)
                            if item.text(0) == node:
                                nodeItem = item
                                break
                        if nodeItem.text(1) != currentPath:
                            item = QTreeWidgetItem(nodeItem)
                            item.setText(0, node)
                            item.setText(1, currentPath)
                            nodeItem = item
                    self.treeDirectory.setCurrentItem(nodeItem)
            else:
                QMessageBox.warning(self, "提示", "路径不存在或无权限")

    def newFile(self):
        filename, ok = QInputDialog.getText(self, '新建文件', '输入文件名：')
        if ok:
            filename = filename.strip()
            for i in range(self.dirListInfo.tableWidget_file.rowCount()):
                if self.dirListInfo.tableWidget_file.item(i, 0).text().strip() == filename:
                    return QMessageBox.warning(self, "提示", "该文件已存在")
            path = self.dirListInfo.currentDirectory + filename
            self.signalNewFile.emit(path)

    def newFileResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            if data["status"]:
                self.dirListInfo.btn_fileRefresh.click()
                QMessageBox.information(self, "提示", "创建成功")
            else:
                QMessageBox.warning(self, "提示", "创建失败")

    def newDir(self):
        dirName, ok = QInputDialog.getText(self, '新建文件夹', '输入文件夹名：')
        if ok:
            dirName = dirName.strip()
            for i in range(self.dirListInfo.tableWidget_file.rowCount()):
                if self.dirListInfo.tableWidget_file.item(i, 0).text().strip() == dirName:
                    return QMessageBox.warning(self, "提示", "该文件夹已存在")
            path = self.dirListInfo.currentDirectory + dirName
            self.signalNewDir.emit(path)

    def deleteFiles(self):
        files = []
        for selected in self.dirListInfo.tableWidget_file.selectedRanges():
            for i in range(selected.topRow(), selected.bottomRow() + 1):
                files.append(self.dirListInfo.currentDirectory + self.dirListInfo.tableWidget_file.item(i, 0).text())
        self.signalDeleteFiles.emit(files)

    def deleteFilesResult(self, result):
        print(result)
        if result["status"]:
            status = result["data"]["status"]
            ok, error = [], []
            for file in status.keys():
                ok.append(file) if status[file] else error.append(file)
            info = ""
            if ok:
                info = ",".join(ok) + "删除成功\n"
            if error:
                info = info + ",".join(error) + "删除失败"
            QMessageBox.information(self, "提示", info)
            self.dirListInfo.btn_fileRefresh.click()

    def modifyFileTime(self):
        row = self.dirListInfo.tableWidget_file.currentRow()
        oldTime = self.dirListInfo.tableWidget_file.item(row, 1).text()
        filepath = self.dirListInfo.currentDirectory + self.dirListInfo.tableWidget_file.item(row, 0).text()
        newTime, ok = QInputDialog.getText(self, "修改时间戳", "输入时间", text=oldTime)
        if ok:
            try:
                time.mktime(time.strptime(newTime, "%Y-%m-%d %H:%M:%S"))
                self.signalModifyFileTime.emit({"file": filepath, "time": newTime})
            except ValueError:
                QMessageBox.warning(self, "提示", "时间格式不正确")

    def modifyFileTimeResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            if data["status"]:
                self.dirListInfo.btn_fileRefresh.click()
                QMessageBox.information(self, "提示", "更改成功")
            else:
                QMessageBox.warning(self, "提示", "更改失败")

    def renameFile(self):
        row = self.dirListInfo.tableWidget_file.currentRow()
        oldName = self.dirListInfo.currentDirectory + self.dirListInfo.tableWidget_file.item(row, 0).text()
        newName, ok = QInputDialog.getText(self, "重命名文件", "输入文件名")
        if ok:
            for i in range(self.dirListInfo.tableWidget_file.rowCount()):
                if self.dirListInfo.tableWidget_file.item(i, 0).text().strip() == newName:
                    reply = QMessageBox.question(self, "提示", "该文件已存在，是否覆盖？",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        return
            newName = self.dirListInfo.currentDirectory + newName
            self.signalRenameFile.emit({"oldName": oldName, "newName": newName})

    def renameFileResult(self, result):
        print(result)
        if result["status"]:
            if result["data"]["status"]:
                self.dirListInfo.btn_fileRefresh.click()
                QMessageBox.information(self, "提示", "重命名成功")
            else:
                QMessageBox.warning(self, "提示", "重命名失败")

    def downloadFile(self):
        row = self.dirListInfo.tableWidget_file.currentItem().row()
        downloadFile = self.dirListInfo.tableWidget_file.item(row, 0).text()
        downloadPath = self.dirListInfo.currentDirectory + downloadFile
        fileName, ok = QFileDialog.getSaveFileName(self, "下载到文件", "download/" + downloadFile, "file(*)")
        if ok:
            self.signalDownloadFile.emit({"downloadFile": downloadPath, "saveFile": fileName})
            self.downloadProgressDialog = QProgressDialog(self)
            self.downloadProgressDialog.canceled.connect(self.signalDownloadFileCancel.emit)
            self.downloadProgressDialog.setWindowTitle('下载文件')
            self.downloadProgressDialog.setLabelText('正在下载 {}'.format(downloadFile))
            self.downloadProgressDialog.setProperty("filename", fileName)

    def downloadFileFinished(self):
        if self.downloadProgressDialog:
            QMessageBox.information(self, "提示", "下载完成")
            filename = self.downloadProgressDialog.property("filename")
            os.startfile(QFileInfo(filename).path())
            self.downloadProgressDialog.hide()
            self.downloadProgressDialog.deleteLater()
            self.downloadProgressDialog = None

    def downloadFileUpdateProgress(self, info):
        if self.downloadProgressDialog:
            if info["maxSize"] > 2147483647:
                self.signalDownloadFileCancel.emit()
                return self.downloadError("文件过大，无法下载")
            self.downloadProgressDialog.setMaximum(info["maxSize"])
            self.downloadProgressDialog.setValue(info["nowSize"])

    def downloadError(self, msg):
        if self.downloadProgressDialog:
            QMessageBox.warning(self, "提示", msg)
            self.downloadProgressDialog.hide()
            self.downloadProgressDialog.deleteLater()
            self.downloadProgressDialog = None

    def uploadFile(self):
        uploadDir = self.dirListInfo.currentDirectory
        uploadFile, ok = QFileDialog.getOpenFileName(self, "上传文件", "/", "file(*)")
        if ok:
            self.uploadProgressDialog = QProgressDialog(self)
            self.uploadProgressDialog.canceled.connect(self.signalUploadFileCancel.emit)
            self.uploadProgressDialog.setWindowTitle("上传文件")
            self.uploadProgressDialog.setLabelText('上传进度:')

            self.signalUploadFile.emit({"uploadDir": uploadDir, "uploadFile": uploadFile})

    def uploadFileUpdateProgress(self, info):
        if self.uploadProgressDialog:
            if info["maxSize"] > 2147483647:
                self.signalUploadFileCancel.emit()
                return self.uploadError("文件过大，无法下载")
            self.uploadProgressDialog.setMaximum(info["maxSize"])
            self.uploadProgressDialog.setValue(info["nowSize"])

    def uploadError(self, msg):
        if self.uploadProgressDialog:
            QMessageBox.warning(self, "提示", msg)
            self.uploadProgressDialog.hide()
            self.uploadProgressDialog.deleteLater()
            self.uploadProgressDialog = None

    def uploadFileFinished(self):
        if self.uploadProgressDialog:
            self.uploadProgressDialog.hide()
            self.uploadProgressDialog.deleteLater()
            self.uploadProgressDialog = None
            QMessageBox.information(self, "提示", "上传成功")
            self.dirListInfo.btn_fileRefresh.click()

    def dirListInfoMenu(self):
        menu = QMenu()

        actionOpen = QAction("打开", self)
        actionOpen.triggered.connect(self.fileOpenDoubleClicked)
        actionRefresh = QAction("刷新", self)
        actionRefresh.triggered.connect(self.fileRefresh)
        menuNew = QMenu("新建", self)
        actionNewFile = QAction("文件", self)
        actionNewFile.triggered.connect(self.newFile)
        actionNewDir = QAction("文件夹", self)
        actionNewDir.triggered.connect(self.newDir)
        menuNew.addActions([actionNewFile, actionNewDir])
        actionDelete = QAction("删除", self)
        actionDelete.triggered.connect(self.deleteFiles)
        actionModifyTime = QAction("修改时间戳", self)
        actionModifyTime.triggered.connect(self.modifyFileTime)
        actionRename = QAction("重命名", self)
        actionRename.triggered.connect(self.renameFile)
        actionDownload = QAction("下载", self)
        actionDownload.triggered.connect(self.downloadFile)
        actionUpload = QAction("上传", self)
        actionUpload.triggered.connect(self.uploadFile)

        selected = self.dirListInfo.tableWidget_file.selectedRanges()
        if not selected:  # 没选中
            actionOpen.setDisabled(True)
            actionDelete.setDisabled(True)
            actionModifyTime.setDisabled(True)
            actionDownload.setDisabled(True)
            actionRename.setDisabled(True)
        elif len(selected) > 1 or selected[0].rowCount() > 1:  # 选中大于一项
            actionModifyTime.setDisabled(True)
            actionRename.setDisabled(True)
            actionDownload.setDisabled(True)
        else:
            row = self.dirListInfo.tableWidget_file.selectedItems()[0].row()
            if self.dirListInfo.tableWidget_file.item(row, 2).text() == "dir":
                actionDownload.setDisabled(True)

        menu.addActions([actionOpen, actionRefresh])
        menu.addSeparator()
        menu.addMenu(menuNew)
        menu.addActions([actionDelete, actionModifyTime, actionRename])
        menu.addSeparator()
        menu.addActions([actionUpload, actionDownload])
        menu.exec_(QCursor.pos())


class DirListInfo(QWidget, Ui_DirListInfo):
    def __init__(self, *args, **kwargs):
        super(DirListInfo, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.currentDirectory = None

        self.initUi()

    def initUi(self):
        self.tableWidget_file.setColumnWidth(0, 250)
        self.tableWidget_file.setColumnWidth(1, 180)
        self.tableWidget_file.setColumnWidth(2, 50)
        self.tableWidget_file.setColumnWidth(3, 100)
        self.tableWidget_file.setContextMenuPolicy(Qt.CustomContextMenu)


class OpenFileInfo(QWidget, Ui_OpenFileInfo):
    signalClosed = pyqtSignal(str)
    signalRefresh = pyqtSignal(str)
    signalSave = pyqtSignal(dict)

    def __init__(self, path, contents, *args, **kwargs):
        super(OpenFileInfo, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.path = path
        self.contents = contents
        self.closeFlag = False
        self.editor = Qsci.QsciScintilla()
        self.initUi()
        self.connectSignal()

    def initUi(self):
        self.setWindowTitle(self.path)
        self.layout_editor.addWidget(self.editor)

        self.editor.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(True)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setUtf8(True)
        self.editor.setMarginType(0, Qsci.QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setText(self.contents)

    def connectSignal(self):
        self.btn_refresh.clicked.connect(self.btnRefreshClicked)
        self.btn_cancel.clicked.connect(self.btnCancelClicked)
        self.btn_save.clicked.connect(self.btnSaveClicked)

    def btnRefreshClicked(self):
        self.signalRefresh.emit(self.path)

    def btnCancelClicked(self):
        self.closeFlag = True
        self.close()

    def btnSaveClicked(self):
        data = {
            "path": self.path,
            "contents": self.editor.text()
        }
        self.signalSave.emit(data)

    def closeEvent(self, evt):
        if not self.closeFlag and self.editor.text() != self.contents:
            result = QMessageBox.question(self, "提示", "是否放弃更改？",
                                          QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if result == QMessageBox.Cancel:
                evt.ignore()
                return

        self.signalClosed.emit(self.path)
        evt.accept()
