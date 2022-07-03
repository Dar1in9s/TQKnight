from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor


class TerminalTab(QTextEdit):
    signalExecuteCommand = pyqtSignal(dict)
    signalExecuteCancel = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TerminalTab, self).__init__(*args, **kwargs)
        self.prompt = ""
        self.currentPath = ""
        self.history = []

        self.currentHistoryNo = 0
        self.beforeCmd = ""
        self.executingFlag = False

        self.initUi()

    def initUi(self):
        self.setStyleSheet("background-color: black; color: white;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDisabled(True)

    def start(self, user, host, path, os):
        if "win" in os.lower():
            self.prompt = "{}> "
        else:
            self.prompt = "{}@{}:{}# ".format(user, host, "{}")
        self.currentPath = path
        self.setText(self.getPrompt())
        self.setDisabled(False)

    def getPrompt(self):
        return self.prompt.format(self.currentPath)

    def updateCommand(self, cmd):
        tmpCursor = self.textCursor()
        tmpCursor.movePosition(QTextCursor.End)
        tmpCursor.select(QTextCursor.LineUnderCursor)
        tmpCursor.removeSelectedText()
        self.insertPlainText(self.getPrompt() + cmd)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def makesureNormalCursor(self):
        cursor = self.textCursor()
        if cursor.blockNumber() + 1 < self.document().lineCount() or cursor.positionInBlock() < len(self.getPrompt()):
            cursor.movePosition(QTextCursor.End)
        if cursor.hasSelection():
            cursor.clearSelection()
        self.setTextCursor(cursor)

    def copySelection(self):
        cursor = self.textCursor()
        QApplication.clipboard().setText(cursor.selection().toPlainText())
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def getPressedCommand(self):
        tmpCursor = self.textCursor()
        tmpCursor.movePosition(QTextCursor.End)
        tmpCursor.select(QTextCursor.LineUnderCursor)
        promptLen = len(self.getPrompt())
        cmd = tmpCursor.selection().toPlainText()[promptLen:].strip()
        return cmd

    def executeCommand(self, cmd):
        self.executingFlag = True
        self.signalExecuteCommand.emit({"cmd": cmd, "path": self.currentPath})

    def executeCommandResult(self, result):
        print(result)
        if result["status"]:
            data = result["data"]
            self.insertPlainText(data["result"])
            self.currentPath = data["path"]
        else:
            self.insertPlainText("Error. (:")
        self.append(self.getPrompt())
        self.executingFlag = False
        self.currentHistoryNo = 0
        self.beforeCmd = ""

    def inputMethodEvent(self, event):  # 保证中英文输入法切换的时候终端不会出错
        if self.executingFlag:
            return
        self.makesureNormalCursor()
        super(TerminalTab, self).inputMethodEvent(event)

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        modifier = event.modifiers()
        key = event.key()

        if modifier == Qt.ControlModifier:
            if key == Qt.Key_C:     # ctrl+c
                self.makesureNormalCursor()
                self.insertPlainText("^C")
                self.append(self.getPrompt())
                self.executingFlag = False
                self.currentHistoryNo = 0
                self.beforeCmd = ""
                self.signalExecuteCancel.emit()
                return
            if self.executingFlag:
                return
            if key == Qt.Key_X:     # ctrl+x
                lastLineSize = len(self.toPlainText().split("\n")[-1])
                totalSize = len(self.document().toPlainText())
                firstLinesSize = totalSize - lastLineSize
                if cursor.hasSelection():
                    if cursor.selectionStart() < firstLinesSize:  # 选区涉及最后一行的上一行
                        return self.copySelection()
                    elif cursor.selectionStart() - firstLinesSize < len(self.getPrompt()):   # 选区涉及提示字符
                        return self.copySelection()
                    # pass
                else:
                    return
            if key == Qt.Key_V:     # ctrl+v
                self.makesureNormalCursor()
                pasteText = QApplication.clipboard().text().strip().split("\n")[0]
                self.insertPlainText(pasteText)
                return
            if key == Qt.Key_Z or key == Qt.Key_Y or key == Qt.Key_Backspace:
                return

        elif self.executingFlag:
            return

        elif modifier == Qt.ShiftModifier:
            if key == Qt.Key_Backspace:
                return
            elif key == Qt.Key_Up or key == Qt.Key_Down:
                return
        else:
            self.makesureNormalCursor()

        if key == Qt.Key_Enter or key == Qt.Key_Return:
            cmd = self.getPressedCommand()
            if not cmd:
                self.append(self.getPrompt())
            else:
                if len(self.history) == 0 or self.history[-1] != cmd:
                    self.history.append(cmd)
                if cmd == "cls" or cmd == "clear":
                    self.clear()
                    self.append(self.getPrompt())
                elif cmd == "exit":
                    self.append(self.getPrompt())
                else:
                    self.executeCommand(cmd)
                    self.append("")
            return

        # 能到这里的都是要输入字符的情况，并且光标都到了最后
        elif key == Qt.Key_Up:
            if self.currentHistoryNo == 0:
                cmd = self.getPressedCommand()
                self.beforeCmd = cmd

            if abs(self.currentHistoryNo) != len(self.history):
                self.currentHistoryNo -= 1
                self.updateCommand(self.history[self.currentHistoryNo])
            return
        elif key == Qt.Key_Down:
            if self.currentHistoryNo == 0:
                self.updateCommand(self.beforeCmd)
            elif self.currentHistoryNo == -1:
                self.currentHistoryNo += 1
                self.updateCommand(self.beforeCmd)
            else:
                self.currentHistoryNo += 1
                self.updateCommand(self.history[self.currentHistoryNo])
            return

        elif key == Qt.Key_Backspace:
            if cursor.positionInBlock() <= len(self.getPrompt()):
                return
        elif key == Qt.Key_Left:
            if cursor.blockNumber() + 1 == self.document().lineCount() and cursor.positionInBlock() == len(self.getPrompt()):
                return

        self.currentHistoryNo = 0
        self.beforeCmd = self.beforeCmd
        super(TerminalTab, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.textCursor().hasSelection():
                self.copySelection()
            else:
                self.makesureNormalCursor()
                pasteText = QApplication.clipboard().text().strip().split("\n")[0]
                self.insertPlainText(pasteText)
            return
        super(TerminalTab, self).mousePressEvent(event)
