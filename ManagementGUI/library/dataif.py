
import time
from threading import Thread, Lock
from library.msgbus import msgbus1


class dataif(Thread,msgbus1):
    def __init__(self):
        Thread.__init__(self)
        self._dataStore = {}
        print('Start DAteninterface')


    def inputData(self,data):
        print('Data',data)
        self.merge(data)

    def merge(self,dict):
       # print('printtree',self.treeRoot.getTree())
        self._merge(self._dataStore,dict)
        self.msgbus_publish('UPDATE',self._dataStore)
        return

    def _merge(self, dict1, dict2):
        print('Merge',dict1,dict2)
        """ Recursively merges dict2 into dict1 """
        if not isinstance(dict1, dict) or not isinstance(dict2, dict):
            return dict2
        for k in dict2:
            print('k',k)
            if k in dict1:
                dict1[k] = self._merge(dict1[k], dict2[k])
            else:
                dict1[k] = dict2[k]
        return dict1

    def outputData(self):
        print(self._dataStore)

    def run(self):
        threadRun = True
        self.msgbus_subscribe('SEND',self.merge)

        while threadRun:
            time.sleep(1)

if __name__ == "__main__":

    data1 = {'TEST1':{'Test1.1':'Test1.1.1'},'Test2':{'Test2.1':'Test2.1.1'}}
    data2 =  {'Test3':{'Test3.1':'Test3.1.1'}}
    data3 =  {'Test3':{'Test3.3':'Test3.1.2'}}
    data4 =  {'Test3':{'Test3.2': {'Test3.2.1':'Test3.2.1.2'}}}

    d = dataif()
    d.merge(data1)
    d.outputData()
    d.merge(data2)
    d.outputData()
    d.merge(data3)
    d.outputData()


