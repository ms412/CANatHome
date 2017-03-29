
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


__app__ = "mqtt2gpio Adapter"
__VERSION__ = "0.8"
__DATE__ = "01.12.2014"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2014 Markus Schiesser"
__license__ = 'GPL v3'

import sys

from library.adapter import *
from library.configfileJson import getConfig
from library.mqttclient import *
from library.msgbus import *
from library.socketcan import socketcanif

from Gateway.library.logging import log_adapter


class manager(msgbus):

    def __init__(self,cfg_file='configfileJson.py.cfg'):

        self._cfg_file = cfg_file

        self._cfg_broker = None
        self._cfg_socket = None
        self._cfg_logging = None

    def read_config(self):
        print('Read Configuration',self._cfg_file)
        cfg_obj = getConfig()
        cfg_obj.open(self._cfg_file)
        self._cfg_broker = cfg_obj.value('BROKER')
        self._cfg_socketcan = cfg_obj.value('SOCKETCAN')
        self._cfg_logging = cfg_obj.value('LOGGING')
        self._cfg_adapter = cfg_obj.value('BROKER')
        print('broker',self._cfg_broker)
        print('socket',self._cfg_socket)

    def start_logging(self):
    #    print('Debug Logging1')
        self._log_thread = log_adapter(self._cfg_logging)
        self._log_thread.start()
     #   self.msgbus_publish('LOG','%s Start Logging Adapter')

    def start_mqttbroker(self):
        self._mqttbroker = mqttbroker(self._cfg_broker)
        self._mqttbroker.start()
        return True

    def start_socketcan(self):
        self._socketcan = socketcanif(self._cfg_socketcan['IF'])
        self._socketcan.start()

    def start_adapter(self):
        self._adapter = adapter(self._cfg_adapter)

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """

    #    self.start_logging()
     #   self.msgbus_publish('LOG','%s Start mqtt2gpio adapter; Version: %s, %s '%('INFO', __VERSION__ ,__DATE__))
        self.read_config()
        self.start_logging()
        self.start_mqttbroker()
        self.start_socketcan()
        self.start_adapter()




if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'configfileJson.py.cfg'

   # print('Configfile',configfileJson.py)
    mgr_handle = manager(configfile)
    mgr_handle.run()