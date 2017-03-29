import sys
import time
from ManagementGUI.library.msgbus import msgbus1
from threading import Thread, Lock
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
#from PyQt5.QtGui import *
#from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
#from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
#from PyQt5 import QtWidgets
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QAction, QApplication, QWidget

data3 = {'TEST1':{'Test1.1':'Test1.1.1'},'Test2':{'Test2.1':'Test2.1.1'}}
data2 =  {'Test3':{'Test3.1':'Test3.1.1'}}

class Window(QWidget, msgbus1):

    def __init__(self):

        QWidget.__init__(self)

        self.msgbus_subscribe('UPDATE', self.updateTree)
        print('start gui xxx')

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
        self.ui.treeWidget.headerItem().setText(0,"mqtt")
      #  self.ui.treeWidget.setContextMenuPolicy(QActionsContextMenu)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.openMenu)

       # self.test1 = uic.loadUi('./gui/test1.ui')
    #    self.widget1 = QVBoxLayout()
       # widget2 = QTabWidget()

       # self.ui.frameWidget.setToolTip('test')
   #     self.ui.dynamicWidget.setLayout(self.widget1)
       # widget1.addWidget(self.test1)

        #time.sleep(15)

        #self.test1 = uic.loadUi('./gui/test2.ui')
        #self.ui.dynamicWidget.setLayout(widget1)
      #  widget1.addWidget(self.test2)
       # self.myLay = QVBoxLayout()

        #   self.ui.treeWidget.headerItem().setText(1, "Gateway")
      #  self.ui.treeWidget.headerItem().setText(2, "BUS")
       # self.ui.treeWidget.headerItem().setText(3, "ID")
       # self.ui.treeWidget.headerItem().setText(4, "Object")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.tr("Object")])

        print('start gui xyz')
        #self.ui.tab.setObjectName("tab45")
    def level1(self):
      #  del (self.widget1)
        self.widget1 = QVBoxLayout()
        self.ui.dynamicWidget.setLayout(self.widget1)

        self.test1 = uic.loadUi('./gui/test1.ui')
        self.widget1.addWidget(self.test1)
      #  self.ui.dynamicWidget.setLayout(widget1)

    def level2(self):
        self.widget1 = QVBoxLayout()
        self.ui.dynamicWidget.setLayout(self.widget1)

        self.test2 = uic.loadUi('./gui/test2.ui')
        self.widget1.addWidget(self.test2)
      #  self.ui.dynamicWidget.setLayout(widget1)

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
        print('fill_item',item,value)
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
        self.ui.treeWidget.clicked.connect(self.connect)
        self.ui.treeWidget.itemClicked.connect(self.itemclicked)

    def connect(self,data):
        print("clicked",data)

    def itemclicked(self,item,column):
        print('itemclicked',item,column)

#    def start_widget(self):
#        d = { 'key1': 'value1',
#  'key2': 'value2',
#  'key3': [1,2,3, { 1: 3, 7 : 9}],
#  'key4': object(),
#  'key5': { 'another key1' : 'another value1',
#            'another key2' : 'another value2'} }
#        self.fill_widget(self.ui.treeWidget,data1)

    def contextMenuEvent(self, event):
         print('event')
         if event.reason() == event.Mouse:
             pos = event.globalPos()
             item = self.itemAt(event.pos())
         else:
             pos = None
             selection = self.selectedItems()
             if selection:
                 item = selection[0]
             else:
                 item = self.currentItem()
                 if item is None:
                     item = self.invisibleRootItem().child(0)
             if item is not None:
                 parent = item.parent()
                 while parent is not None:
                     parent.setExpanded(True)
                     parent = parent.parent()
                 itemrect = self.visualItemRect(item)
                 portrect = self.viewport().rect()
                 if not portrect.contains(itemrect.topLeft()):
                     self.scrollToItem(
                         item, QTreeWidget.PositionAtCenter)
                     itemrect = self.visualItemRect(item)
                 itemrect.setLeft(portrect.left())
                 itemrect.setWidth(portrect.width())
                 pos = self.mapToGlobal(itemrect.center())
         if pos is not None:
             menu = QMenu(self)
             menu.addAction(item.text(0))
             menu.popup(pos)
         event.accept()

    def openMenu(self, position):
        print('openMenu')

        indexes = self.ui.treeWidget.selectedIndexes()
        print('indexes',indexes)
        level = 0
        if len(indexes) > 0:

          #  level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        print('level',level)
        if level == 0:
            print('level_0')
            self.level0 = menu.addAction(self.tr("Add mqtt"))
            self.level0dell = menu.addAction(self.tr("Del mqtt"))
            print('test')
            self.level0.triggered.connect(self.clickLevel0)
       #     self.level0del.clicked.connect(self.clieckLevel0("del"))
          #  self.level1()
       #     action1 = menu.addAction('Add Gateway')

        #    action2 = menu.addAction('Del Gateway')
        #    print('action',action2)
          #  action1.triggered.connect(self.test1)
         #   action2.triggered.connect(self.test2)

        elif level == 1:
            menu.addAction(QAction('Add Bus',self))
            menu.addAction(QAction('Del Bus',self))
            self.level2()
        elif level == 2:
            menu.addAction(self.tr("Add Node"))
        elif level == 3:
            menu.addAction(QAction('Object',self))
            menu.addSeparator()
            menu.addAction(QAction('Add Bus',self))


        menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))

    def clickLevel0(self):
        print('?')
        print('clicked level0')
        self.level1()

class maingui(Thread):
    def __init__(self):
        Thread.__init__(self)
      #  self.app
        print('gui start 123')


    def run(self):
        print('GUI Start')
        app = QtWidgets.QApplication(sys.argv)
        window = Ui()
     #   window.start_widget()
      #  window.start_widget()
        sys.exit(app.exec_())

