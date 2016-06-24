import sys
import time
from threading import Thread, Lock
from library.msgbus import msgbus1
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys

class Ui(QtWidgets.QMainWindow, msgbus1):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('mainwindow.ui')
        self.ui.show()

        self.msgbus_subscribe('UPDATE', self.updateTree)
        print('start gui')




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

