import ujson

from Node.system.canIf import canIf


class canWrapper(object):
    def __init__(self,bitrate,filter,callback):
        self._commIf = canIf()
        self._commIf.bitrate(bitrate)
        self._commIf.filter(filter)
        self._callback = callback
        print('start can if')

    def run(self):
        while True:
            (state, data) = self._commIf.rxString()
            if 'COMPLET' in state:
                self._callback(ujson.loads(data))
                #				msg = ujson.loads(data)
                #                object = msg.get('OBJECT')
                #                method = msg.get('METHOD')
                #                value = msg.get('VALUE')
         #       print('DATA', state, data)

            yield

    def sink(self, msg):
        self._commIf.txString(ujson.dumps(msg))