
import time
from threading import Thread, Lock
from ManagementGUI.library.msgbus import msgbus1


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


class monitor(msgbus1):
    def __init__(self):
        self._store = []
        self._inventar = {}

    def dict_compare(self,d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        equal = (d1 == d2)
        return added, removed, modified, same, equal

    def dict_merge(self,dct, merge_dct):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``dct``.
        :param dct: dict onto which the merge is executed
        :param merge_dct: dct merged into dct
        :return: None
        """
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict)
                    and isinstance(merge_dct[k], dict)):
                self.dict_merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]
        return dct

    def list2nestdic(self,mylist):
        print(mylist)
        result = {}
        for name in reversed(mylist):
            result = {name: result}

        return result

    def lookup(self,data):
     #   if len(self._store):
        result = False
        for item in self._store:
            print('itemxx',item)
            added, removed, modified, same, equal= self.dict_compare(item,data)
            print('Same',equal)
            result = equal
            if False:
                return result
        return result


    def uptime(self,data):
        self.__store={}
        print('MQTT_RY',data)
        print('STORE',self._store)
        message = data.get('MESSAGE').decode("utf-8")
        channel = data.get('CHANNEL')

        channellist = channel.split('/')
        Gateway = channellist[1]
        CANbus = channellist[2]
        NodeID = channellist[3]
        Object = channellist[4]
        Method = channellist[5]
        tmplist = []
        tmplist.append(channellist[1])
        tmplist.append(channellist[2])
        tmplist.append(channellist[3])
        tmplist.append(channellist[4])
        tmplist.append(channellist[5])


      #  print('monitor',Gateway,CANbus,NodeID,Object,Method)

       # self.__store['Gateway']=Gateway
       # self.__store['CANbus']=CANbus
        #self.__store['NodeID']=NodeID
       # self.__store['Object']=Object
        #self.__store['Method']=Method

        print('templist',tmplist)

        tempdict = self.list2nestdic(tmplist)
        print('dictlist',tempdict)

        self.dict_merge(self._inventar, tempdict)

        print('inventar',self._inventar)
        self.msgbus_publish('UPDATE',self._inventar)

      #  if not self.lookup(self.__store):
      #      print('Store11',self.__store,self._store)
       #     self._store.append(self.__store)

        #self.update()

    def update(self):
        newdict = {}
        tmplist = []
        print('Store22',self._store)
        for item in self._store:
            tmplist.append(item.get('Gateway'))
            tmplist.append(item.get('CANbus'))
            tmplist.append(item.get('NodeID'))
            tmplist.append(item.get('Object'))
            print('templist',tmplist)
            tempdict = self.list2nestdic(tmplist)
            tempdict = self.dict_merge(newdict,tempdict)
            print('update',tempdict)
            self.msgbus_publish('UPDATE',tempdict)
            newdict = tempdict
        return tmplist


