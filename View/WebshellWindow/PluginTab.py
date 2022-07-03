from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter, QStackedWidget, QHBoxLayout, QListWidgetItem, QPushButton,\
    QButtonGroup
from PyQt5.QtGui import QIcon
from config import Config
from View.qss import loadQSS
import importlib
import os


class PluginTab(QWidget):
    def __init__(self, *args, **kwargs):
        super(PluginTab, self).__init__(*args, **kwargs)
        self.spliter = QSplitter()
        self.layout_ = QHBoxLayout(self)
        self.listCatalog = QListWidget()
        self.stackedWidget = QStackedWidget()
        self.pluginsWidgetList = []
        self.btnGroup = QButtonGroup()
        self.connectSignal()
        self.initUi()

    def connectSignal(self):
        self.listCatalog.currentItemChanged.connect(self.currentPluginChanged)

    def initUi(self):
        self.btnGroup.setExclusive(True)
        self.layout_.setContentsMargins(0, 10, 0, 0)
        self.layout_.addWidget(self.spliter)
        self.spliter.addWidget(self.listCatalog)
        self.spliter.addWidget(self.stackedWidget)
        self.spliter.setChildrenCollapsible(False)
        self.listCatalog.setMaximumWidth(180)
        self.listCatalog.setMinimumWidth(120)
        self.setStyleSheet(loadQSS("pluginTab.qss"))

    def loadPlug(self, service):
        if self.pluginsWidgetList:
            return
        for plug in Config.plugList:
            try:
                btn = QPushButton(plug["title"])
                btn.setCheckable(True)
                btn.setObjectName("menu")
                btn.setIcon(QIcon("{}/plugins/{}/{}".format(os.getcwd(), plug["name"], plug["logo"])))
                self.btnGroup.addButton(btn)

                item = QListWidgetItem()
                self.listCatalog.addItem(item)
                self.listCatalog.setItemWidget(item, btn)

                _plug = importlib.import_module("plugins.{}.main".format(plug["name"]))
                _plugClass = getattr(_plug, plug["class"])
                _plugInstance = _plugClass(service)
                self.pluginsWidgetList.append(_plugInstance)
                self.stackedWidget.addWidget(_plugInstance)
            except Exception as e:
                print(e)
        self.listCatalog.setCurrentRow(0)

    def currentPluginChanged(self):
        currenIndex = self.listCatalog.currentIndex()
        self.listCatalog.indexWidget(currenIndex).setChecked(True)
        self.stackedWidget.setCurrentIndex(currenIndex.row())
