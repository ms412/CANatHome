import sys
import time
from library.msgbus import msgbus1
from threading import Thread, Lock
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtWidgets


data1 = {'TEST1':{'Test1.1':'Test1.1.1'},'Test2':{'Test2.1':'Test2.1.1'}}
data2 =  {'Test3':{'Test3.1':'Test3.1.1'}}

class Window(QWidget, msgbus1):

    def __init__(self):

        QWidget.__init__(self)

        self.msgbus_subscribe('UPDATE', self.updateTree)
        print('start gui')

        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.model = QStandardItemModel()
       # self.updateTree()
      #  self.addItems(self.model, data)
       # self.addItems(self.model,data2)
        self.treeView.setModel(self.model)

        self.model.setHorizontalHeaderLabels([self.tr("Object")])

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)


    def updateTree(self, data):
        print('Update')
        self.model.clear()
        self.addItems(self.model,data)

    def addItems(self,parent, elements):
        print('Element',elements)
        if not isinstance(elements, dict):
            item = QStandardItem(elements)
            parent.appendRow(item)

        else:
            for key, value in elements.items():
                print (key,value)
                item = QStandardItem(key)
                parent.appendRow(item)
                print('parent',parent)
                self.addItems(item, value)


    def openMenu(self, position):

        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))

        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.treeView.viewport().mapToGlobal(position))


class maingui(Thread):
    def __init__(self):
        Thread.__init__(self)
      #  self.app
        print('gui start')


    def run(self):
        print('GUI Start')
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())

