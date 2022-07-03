from PyQt5.QtWidgets import QWidget, QSplitter, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import Qsci
from .ui_CodeEditor import Ui_CodeEditor
from .images_rc import *
import base64
import json
import os


class CodeExecute(QWidget):
    def __init__(self, service, *args, **kwargs):
        super(CodeExecute, self).__init__(*args, **kwargs)
        self.layout_ = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Vertical)
        self.codeEditor = CodeEditor()
        self.resultEditor = QTextEdit()
        self.service = service
        self.initUi()
        self.connectSignal()
        self.resultContents = ""

    def initUi(self):
        self.layout_.addWidget(self.splitter)
        self.splitter.addWidget(self.codeEditor)
        self.splitter.addWidget(self.resultEditor)
        self.splitter.setChildrenCollapsible(False)
        self.resultEditor.setReadOnly(True)

    def connectSignal(self):
        self.codeEditor.btn_run.clicked.connect(self.executeCode)
        self.codeEditor.btn_clear.clicked.connect(self.clearEditor)
        self.codeEditor.comboBox_readType.currentIndexChanged.connect(self.showTypeChanged)

    def executeCode(self):
        if not self.service.os:
            return
        code = self.codeEditor.editor.text().strip()
        with open(os.path.dirname(__file__)+"/payload/codeExecute.php", "rb") as f:
            payload = f.read().replace(b"__CODE__", base64.b64encode(code.encode()))
        data = {
            "code": base64.b64encode(payload).decode()
        }
        data = self.service.AESEncrypt(self.service.aesKey, json.dumps(data))
        self.service.nam.finished.connect(self.executeCodeResult)
        self.service.doPOST(data)

    def executeCodeResult(self, reply):
        result = self.service.parseReply(reply)
        print(result)
        self.resultEditor.clear()
        if result["status"]:
            self.resultContents = result["data"]["result"]
            if self.codeEditor.comboBox_readType.currentIndex() == 0:
                self.resultEditor.setPlainText(result["data"]["result"])
            else:
                self.resultEditor.setText(result["data"]["result"])
        else:
            self.resultEditor.setText("error")
        self.service.nam.finished.disconnect(self.executeCodeResult)

    def clearEditor(self):
        self.codeEditor.editor.clear()
        self.resultEditor.clear()

    def showTypeChanged(self):
        if self.codeEditor.comboBox_readType.currentIndex() == 0:
            self.resultEditor.setPlainText(self.resultContents)
        else:
            self.resultEditor.setText(self.resultContents)


class CodeEditor(QWidget, Ui_CodeEditor):
    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.editor = Qsci.QsciScintilla()
        self.editor.setText("phpinfo();")
        self.layout_editor.addWidget(self.editor)
