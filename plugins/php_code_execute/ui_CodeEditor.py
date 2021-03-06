# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CodeEditor.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodeEditor(object):
    def setupUi(self, CodeEditor):
        CodeEditor.setObjectName("CodeEditor")
        CodeEditor.resize(685, 419)
        self.gridLayout = QtWidgets.QGridLayout(CodeEditor)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_clear = QtWidgets.QPushButton(CodeEditor)
        self.btn_clear.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 0, 1, 1, 1)
        self.btn_run = QtWidgets.QPushButton(CodeEditor)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/execute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_run.setIcon(icon1)
        self.btn_run.setObjectName("btn_run")
        self.gridLayout.addWidget(self.btn_run, 0, 0, 1, 1)
        self.comboBox_readType = QtWidgets.QComboBox(CodeEditor)
        self.comboBox_readType.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_readType.setObjectName("comboBox_readType")
        self.comboBox_readType.addItem("")
        self.comboBox_readType.addItem("")
        self.gridLayout.addWidget(self.comboBox_readType, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(CodeEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.widget = QtWidgets.QWidget(CodeEditor)
        self.widget.setObjectName("widget")
        self.layout_editor = QtWidgets.QHBoxLayout(self.widget)
        self.layout_editor.setContentsMargins(0, 0, 0, 0)
        self.layout_editor.setSpacing(0)
        self.layout_editor.setObjectName("layout_editor")
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 5)

        self.retranslateUi(CodeEditor)
        QtCore.QMetaObject.connectSlotsByName(CodeEditor)

    def retranslateUi(self, CodeEditor):
        _translate = QtCore.QCoreApplication.translate
        CodeEditor.setWindowTitle(_translate("CodeEditor", "Form"))
        self.btn_clear.setText(_translate("CodeEditor", "??????"))
        self.btn_run.setText(_translate("CodeEditor", "??????"))
        self.comboBox_readType.setItemText(0, _translate("CodeEditor", "?????????"))
        self.comboBox_readType.setItemText(1, _translate("CodeEditor", "html??????"))
        self.label.setText(_translate("CodeEditor", "   ????????????:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CodeEditor = QtWidgets.QWidget()
    ui = Ui_CodeEditor()
    ui.setupUi(CodeEditor)
    CodeEditor.show()
    sys.exit(app.exec_())
