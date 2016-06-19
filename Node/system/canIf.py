from pyb import CAN
import array
import utime
import ujson


class canIf(object):
    def __init__(self,canId = 1):
   #     self._canIf = CAN(1, CAN.NORMAL, extframe=False, prescaler=16, sjw=1, bs1=14, bs2=6)
   #     self._canIf.setfilter(0, CAN.LIST16, 0, (124, 124, 124, 124))
        self._canIf = None
        self._canId = canId
        self._canAddr = 255

        self._rxTimeout = 5

        self._FRM_BYTE = 0x7D
        self._ESC_BYTE = 0x7E

        self._txByte = 0
        self._rxByte = 0
        self._txFrame = 0
        self._rxFrame = 0

    def bitrate(self, bitrate = 125):
        if bitrate == 125:
            # 125kpbs, PCLK1@42000000
            self._canIf = CAN(self._canId, CAN.NORMAL, extframe=False, prescaler=16, sjw=1, bs1=14, bs2=6)
            print('set can speed', bitrate)
        elif bitrate == 250:
            ''' Init for 250 kbps <=> bit time 4 µs. If 42 MHz clk is prescaled by 21, we get 8 subparts 'tq'
            of a bit time from theese parts (# tq): sync(1) + bs1(5) + bs2(2) = 8 * tq = 4µs => 250 kbps'''
            self._canIf = CAN(self._canId, CAN.NORMAL, extframe=False, prescaler=21, sjw=1, bs1=5, bs2=2)
        else:
            print('CAN speed not found')

        self._canIf.initfilterbanks(1)
        return True

    def filter(self, address):
        canfilterList = []
        for x in range(0, 4):
            canfilterList.append(address)
            #  mylist.append(123)
        self._canAddr = address
        self._canIf.setfilter(0, CAN.LIST16, 0, canfilterList)
        print('Filter',self._canAddr)
        return True

    def buffer(self,buffer = 0):
        return self._canIf.any(buffer)

    def receive(self):
        timeout = False
        timeoutValue = utime.time() + self._rxTimeout

        state = 'INIT'
        data = []

        if self._canIf.any(0):
            print('Data')
            while not(timeout):
                if self._canIf.any(0):
                    (id,type,fmi,canframe) = self._canIf.recv(0)
                    self._rxFrame += 1
                    for item in canframe:
                        self._rxByte += 1

#                    ''' Start Frame '''
                        if item == self._FRM_BYTE and state in 'INIT':
                            state = 'RUN'
                            print(state,item)
                          #  data.append(item)
#                    ''' End Frame '''
                        elif item == self._FRM_BYTE and state in 'RUN':
                            state = 'COMPLET'
                            print(state,item)
                          #  data.append(item)
                            return(state,data)
#                    ''' Stuffin Byte'''
                        elif item == self._ESC_BYTE and state in 'RUN':
                            state = 'STUFFING'
                            print(state,item)
  #                   ''' un-Stuffing'''
                        elif state in 'STUFFING':
                            data.append(item ^ 0x20)
                            state = 'RUN'
                            print(state,item)
                        else:
                            data.append(item)
   #          ''' Timeout '''
                elif utime.time()> timeoutValue:
                    state = 'TIMEOUT'
                    timeout = True
                    return(state,data)
        else:
            state = 'NODATA'
       #     print('NoData')

        return(state,data)

    def transmit(self, data):
        size = len(data)
     #   print('Transmit',size,data)
        # self._arrayTx =[]
        state = 'INIT'
        buffer = array.array('B', [])
        buffer.append(self._FRM_BYTE)
        state = 'RUN'
        length = 0

        for item in data:
           # print('tt',size,item,len(self._arrayTx))
            size = size - 1
    #        print(len(buffer),item)

            if len(buffer) == 8:
        #        print('test', buffer)
                #self._canIf.send(buffer, self._address, timeout=500)
                self.canSend(buffer)

                buffer = array.array('B', [])
                #     print('array',len(self._arrayTx))
                #print('state', self._state,self._arrayTx)

            #if 'INIT' in state:
            #    buffer.append(self._FRM_BYTE)
            #    buffer.append(item)
            #    state = 'RUN'
            if 'RUN' in state:
                if item in (self._FRM_BYTE, self._ESC_BYTE):
                    buffer.append(self._ESC_BYTE)
         #           print(len(buffer),buffer)
                    if len(buffer) == 8:
                       # self._canIf.send(buffer, self._address, timeout=500)
                        self.canSend(buffer)
                        buffer = array.array('B', [])

                    buffer.append(item ^ 0x20)
                    if len(buffer) == 8:
                        self.canSend(buffer)
                        buffer = array.array('B', [])
                        
                else:
                    buffer.append(item)
                    #  elif size <= 0:
                    #     print('end')

        buffer.append(self._FRM_BYTE)
        self.canSend(buffer)
      #  self._canIf.send(buffer, self._address, timeout=500)

        return size

    def canSend(self,buffer):
       # print('canSend',buffer)
        self._canIf.send(buffer, self._canAddr, timeout=500)
        self._txByte += len(buffer)
        self._txFrame += 1
        return True

    def maintenance(self):
        maint = {}
        maint['TX-BYTE'] = self._txByte
        maint['RX-BYTE'] = self._rxByte
        maint['TX-FRAME'] = self._txFrame
        maint['RX-FRAME'] = self._rxFrame

        return maint
		
    def txString(self,str):
        data = []
        for item in str:
            #print(item)
            data.append(ord(item))
			
        return(self.transmit(data))
		
    def rxString(self):
        #print('StringRx')
        str = ''
        (state,data) = self.receive()
		
        if 'COMPLET' in state:
            str = ''.join(chr(i) for i in data)
            print('String',str)
			
        return(state,str)


