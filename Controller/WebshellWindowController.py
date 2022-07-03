from PyQt5.QtCore import QObject
from View import WebshellWindow
from Core import WebshellService, Socks5Service


class WebshellWindowController(QObject):
    def __init__(self, webshell, proxy, *args, **kwargs):
        super(WebshellWindowController, self).__init__(*args, **kwargs)
        self.webshellService = WebshellService(webshell, proxy)
        self.webshellWindow = WebshellWindow(webshell, proxy)
        self.socks5Service = None

        self.connectSignal()
        self.webshellService.shackHand()

    def connectSignal(self):
        self.webshellService.signalShackHandResult.connect(self.getBaseInfo)
        self.webshellService.signalGetBaseInfoResult.connect(self.webshellWindow.getBaseInfoResult)

        self.webshellWindow.signalClose.connect(self.webshellService.closeSession)
        self.webshellService.signalSessionClosed.connect(self.webshellWindow.signalRealClose.emit)

        self.webshellWindow.fileManageTab.signalListDirectory.connect(self.webshellService.listDirectory)
        self.webshellService.signalListDirectoryResult.connect(self.webshellWindow.fileManageTab.listDirectoryResult)

        self.webshellWindow.fileManageTab.signalOpenFile.connect(self.webshellService.readFile)
        self.webshellService.signalReadFileResult.connect(self.webshellWindow.fileManageTab.openFileResult)

        self.webshellWindow.fileManageTab.signalUpdateFile.connect(self.webshellService.updateFile)
        self.webshellService.signalUpdateFileResult.connect(self.webshellWindow.fileManageTab.saveFileResult)

        self.webshellWindow.fileManageTab.signalOpenPath.connect(self.webshellService.detectPath)
        self.webshellService.signalDetectPathResult.connect(self.webshellWindow.fileManageTab.openPathResult)

        self.webshellWindow.fileManageTab.signalNewFile.connect(self.webshellService.newFile)
        self.webshellService.signalNewFileResult.connect(self.webshellWindow.fileManageTab.newFileResult)

        self.webshellWindow.fileManageTab.signalNewDir.connect(self.webshellService.newDir)
        self.webshellService.signalNewDirResult.connect(self.webshellWindow.fileManageTab.newFileResult)

        self.webshellWindow.fileManageTab.signalDeleteFiles.connect(self.webshellService.deleteFiles)
        self.webshellService.signalDeleteFilesResult.connect(self.webshellWindow.fileManageTab.deleteFilesResult)

        self.webshellWindow.fileManageTab.signalModifyFileTime.connect(self.webshellService.modifyFileTime)
        self.webshellService.signalModifyFileTimeResult.connect(self.webshellWindow.fileManageTab.modifyFileTimeResult)

        self.webshellWindow.fileManageTab.signalRenameFile.connect(self.webshellService.renameFile)
        self.webshellService.signalRenameFileResult.connect(self.webshellWindow.fileManageTab.renameFileResult)

        self.webshellWindow.fileManageTab.signalDownloadFile.connect(self.webshellService.downloadFile)
        self.webshellWindow.fileManageTab.signalDownloadFileCancel.connect(self.webshellService.downloadCancel)
        self.webshellService.signalDownloadFinished.connect(self.webshellWindow.fileManageTab.downloadFileFinished)
        self.webshellService.signalDownloadUpdateProgress.connect(self.webshellWindow.fileManageTab.downloadFileUpdateProgress)
        self.webshellService.signalDownloadError.connect(self.webshellWindow.fileManageTab.downloadError)

        self.webshellWindow.fileManageTab.signalUploadFile.connect(self.webshellService.uploadFile)
        self.webshellWindow.fileManageTab.signalUploadFileCancel.connect(self.webshellService.uploadFileCancel)
        self.webshellService.signalUploadUpdateProgress.connect(self.webshellWindow.fileManageTab.uploadFileUpdateProgress)
        self.webshellService.signalUploadFileFinished.connect(self.webshellWindow.fileManageTab.uploadFileFinished)
        self.webshellService.signalUploadError.connect(self.webshellWindow.fileManageTab.uploadError)

        self.webshellWindow.terminalTab.signalExecuteCommand.connect(self.webshellService.executeCmd)
        self.webshellWindow.terminalTab.signalExecuteCancel.connect(self.webshellService.executeCmdCancel)
        self.webshellService.signalExecuteCmdResult.connect(self.webshellWindow.terminalTab.executeCommandResult)

        self.webshellWindow.databaseTab.signalConnectDatabase.connect(self.webshellService.connectDatabase)
        self.webshellService.signalConnectDatabaseResult.connect(self.webshellWindow.databaseTab.connectDatabaseResult)

        self.webshellWindow.databaseTab.signalShowTables.connect(self.webshellService.showTables)
        self.webshellService.signalShowTablesResult.connect(self.webshellWindow.databaseTab.showTablesResult)

        self.webshellWindow.databaseTab.signalSelectTableAttr.connect(self.webshellService.selectTableAttr)
        self.webshellService.signalSelectTableAttrResult.connect(self.webshellWindow.databaseTab.selectTableAttrResult)

        self.webshellWindow.databaseTab.signalSelectTableData.connect(self.webshellService.selectTableData)
        self.webshellService.signalSelectTabledataResult.connect(self.webshellWindow.databaseTab.selectTableDataResult)

        self.webshellWindow.databaseTab.sqlExecuteWindow.signalExecuteSQL.connect(self.webshellService.executeSQL)
        self.webshellService.signalExecuteSQLResult.connect(self.webshellWindow.databaseTab.sqlExecuteWindow.executeSQLResult)

        self.webshellWindow.intranetProxyTab.signalHttpSocksOpen.connect(self.httpSocksOpen)

        self.webshellWindow.signalLoadPluginRequest.connect(lambda: self.webshellWindow.pluginTab.loadPlug(self.webshellService))

    def getBaseInfo(self, result):
        print(result)
        if result["status"]:
            self.webshellService.getBaseInfo()

    def httpSocksOpen(self, port):
        self.socks5Service = Socks5Service(port, self.webshellService)
        self.socks5Service.start()

    def show(self):
        self.webshellWindow.show()
        self.webshellWindow.activateWindow()
