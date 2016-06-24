import sys
import time
from ManagementGUI.library.msgbus import msgbus1
from threading import Thread, Lock
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
#from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
#from PyQt5 import QtWidgets
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *


data3 = {'TEST1':{'Test1.1':'Test1.1.1'},'Test2':{'Test2.1':'Test2.1.1'}}
data2 =  {'Test3':{'Test3.1':'Test3.1.1'}}

class Window(QWidget, msgbus1):

    def __init__(self):

        QWidget.__init__(self)

        self.msgbus_subscribe('UPDATE', self.updateTree)
        print('start gui')

   #     self.treeView = QTreeView()
    #    self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
     #   self.treeView.customContextMenuRequested.connect(self.openMenu)

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
            action1 = menu.addAction('Add Gateway')

            action2 = menu.addAction('Del Gateway')
            print('action',action2)
            action1.triggered.connect(self.test1)
            action2.triggered.connect(self.test2)

        elif level == 1:
            menu.addAction(QAction('Add Bus',self))
            menu.addAction(QAction('Del Bus',self))
        elif level == 2:
            menu.addAction(self.tr("Add Node"))
        elif level == 3:
            menu.addAction(QAction('Object',self))
            menu.addSeparator()
            menu.addAction(QAction('Add Bus',self))
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def test1(self):
        print('1test')

    def test2(self):
        print('2test')

class Ui(QtWidgets.QMainWindow, msgbus1):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('./gui/mainwindow.ui')
        self.ui.show()
     #   self.ui.setupUi(self

        self.msgbus_subscribe('UPDATE', self.updateTree)

        header=QTreeWidgetItem(["Tree"])
        self.ui.treeWidget.setHeaderItem(header)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.tr("Object")])

        print('start gui')
        #self.ui.tab.setObjectName("tab45")

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

    def fill_item(self,item, value):
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, str(val))
                    child.setExpanded(True)
        else:
            child = QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)

    def fill_widget(self,widget, value):
        widget.clear()
        self.fill_item(widget.invisibleRootItem(), value)

    def updateTree(self,data):
        print('updateTree',data)
        self.fill_widget(self.ui.treeWidget,data)

    def start_widget(self):
        d = { 'key1': 'value1',
  'key2': 'value2',
  'key3': [1,2,3, { 1: 3, 7 : 9}],
  'key4': object(),
  'key5': { 'another key1' : 'another value1',
            'another key2' : 'another value2'} }
        self.fill_widget(self.ui.treeWidget,data1)

class maingui(Thread):
    def __init__(self):
        Thread.__init__(self)
      #  self.app
        print('gui start')


    def run(self):
        print('GUI Start')
        app = QtWidgets.QApplication(sys.argv)
        window = Ui()
     #   window.start_widget()
      #  window.start_widget()
        sys.exit(app.exec_())

