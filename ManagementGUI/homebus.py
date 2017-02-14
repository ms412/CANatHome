#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


__app__ = "Homebus Adapter"
__VERSION__ = "0.1"
__DATE__ = "18.06.2016"
__author__ = "Markus Schiesser"
__contact__ = "Markus.Schiesser@swisscom.com"
__copyright__ = "Copyright (C) 2015 Markus Schiesser"
__license__ = 'GPL v3'

import sys


from ManagementGUI.library.mqttclient import *
from ManagementGUI.library.msgbus import msgbus1
from ManagementGUI.gui.mainwindow import maingui
from ManagementGUI.library.dataif import dataif, monitor



class manager(msgbus1):

    def __init__(self):

        self._cfg_broker = None
        self._cfg_gerneral = None
        self._cfg_instrument = None
        self._dataif = None

        self._monitor = None

        self.msgbus_subscribe('LOG',self.log)

    def log(self,data):
        print('LOG:',data)

    def start_gui(self):
        self._gui = maingui()
        self._gui.start()

    def start_mqttbroker(self):
        self._cfg_broker={'HOST':'192.168.2.50','SUBSCRIBE':'/XX/'}
        self._mqttbroker = mqttbroker(self._cfg_broker)
        self.msgbus_subscribe('MQTT_RX',self.test2)
        self._mqttbroker.start()
        return True

    def dataInterface(self):
        self._dataif = dataif()
        self._dataif.start()
        print(self._dataif)

    def test2(self,data):
        print('mqtt Rx',data)
        self._monitor.uptime(data)


    def test1(self,data):
        print(data)
        self.msgbus_publish('UPDATE',data)
     #   self._dataif.merge(data)

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """

    #    self.start_logging()
     #   self.msgbus_publish('LOG','%s Start mqtt2gpio adapter; Version: %s, %s '%('INFO', __VERSION__ ,__DATE__))

        self._monitor = monitor()

        self.start_mqttbroker()
        self.start_gui()
        time.sleep(5)
        self.dataInterface()

        print('test')
      #  self.test1({'Test1':{'Test1.1':{'Test1.1.1':{'Test1.1.1.1':'Test1.1.1.1'}},'Test1':{'Test2.1':'Test2.1.1'}}})
       # time.sleep(5)
        #self.test1({'Test1':{'Test3.1':'Test3.1.1'}})
       # time.sleep(5)
        #self.test1({'Test1':{'Test3.3':'Test3.1.2'}})
        #time.sleep(5)
        #self.test1({'Test1':{'Test3.2': {'Test3.2.1':'Test3.2.1.2'}}})

      #  self.msgbus_publish('MQTT_TX','123456')

#        self.msgbus_subscribe('CAN_RX',self.canif)




if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        print('no commandline ')
        cfgfile = sys.argv[1]
    else:
        print('read default file')
        cfgfile = 'gpib2mqtt.cfg'

    mgr_handle = manager()
    mgr_handle.run()