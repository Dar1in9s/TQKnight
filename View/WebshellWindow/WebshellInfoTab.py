from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from View.WebshellWindow.UI import Ui_WebshellInfoTab


class WebshellInfoTab(Ui_WebshellInfoTab, QWidget):
    def __init__(self, *args, **kwargs):
        super(WebshellInfoTab, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.splitter = QSplitter()
        self.layout_spliter.addWidget(self.splitter)
        self.containerEnvInfo = QWidget()
        self.containerNetInfo = QWidget()
        self.layoutEnvInfo = QVBoxLayout(self.containerEnvInfo)
        self.layoutEnvInfo.setContentsMargins(0, 0, 0, 0)
        self.layoutNetInfo = QVBoxLayout(self.containerNetInfo)
        self.layoutNetInfo.setContentsMargins(0, 0, 0, 0)

        self.labelEnvInfo = QLabel("环境变量：")
        self.labelNetInfo = QLabel("网络配置信息：")
        self.textEditEnvInfo = QTextEdit()
        self.textEditNetInfo = QTextEdit()
        self.textEditEnvInfo.setReadOnly(True)
        self.textEditNetInfo.setReadOnly(True)
        self.layoutEnvInfo.addWidget(self.labelEnvInfo)
        self.layoutEnvInfo.addWidget(self.textEditEnvInfo)
        self.layoutNetInfo.addWidget(self.labelNetInfo)
        self.layoutNetInfo.addWidget(self.textEditNetInfo)

        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.containerNetInfo)
        self.splitter.addWidget(self.containerEnvInfo)
        self.splitter.setChildrenCollapsible(False)

    def initData(self, data):
        self.lineEdit_url.setText(data["url"])
        self.lineEdit_type.setText(data["type"])
        self.lineEdit_time.setText(data["time"])
        self.lineEdit_proxy.setText(data["name"])

    def setBaseInfo(self, data):
        self.lineEdit_os.setText(data["os"])
        self.lineEdit_hostname.setText(data["host"])
        self.lineEdit_phpVersion.setText(data["phpVersion"])
        self.textEditNetInfo.setText(data["ipInfo"].strip())
        self.textEditEnvInfo.clear()
        for env in data["env"].keys():
            self.textEditEnvInfo.append("{}: {}".format(env, data["env"][env]))

