import json

from Gateway.library.msgbus import msgbus


class adapter(msgbus):

    def __init__(self,config):

        self._config = config
        self.msgbus_subscribe('MQTT_RX',self.mqttif)
        self.msgbus_subscribe('CAN_RX',self.canif)

    def mqttif(self,data):
        print('MQTT_RY',data)
        message = data.get('MESSAGE').decode("utf-8")
        channel = data.get('CHANNEL')

        channellist = channel.split('/')
        gateway = channellist[1]
        canbus = channellist[2]
        canID = channellist[3]
        object = channellist[4]
        method = channellist[5]
   #     network = channellist[1]
    #    address = channellist[2]
     #   rcpcall = channellist[3]


        msg = {}
        msg['VALUE'] = message
        msg['OBJECT'] = object
        msg['METHOD'] = method

        jmessage = json.dumps(msg)
        print('Message', gateway, canbus, canID, jmessage)

       # print('rcpcall',message)

      #  rcpmsg ='/' + rcpcall + message
       # print('Network',network,address,rcpcall,rcpmsg)
        #msg = 'Received mqtt call'
    #    self.msgbus_publish('LOG','%s SocketCanIF: %s CAN ID: %d Message: %s '%('DEBUG',msg,network,address,rcpmsg))
        self.msgbus_publish('CAN_TX',canbus,canID,jmessage)


    def canif(self,addr,data):
        mqtt_data= {}
        mqttChannel = []
        message=''.join(chr(i) for i in data)
        print('CANif',addr,data)
        jdata = json.loads(message)
        print('jdata',jdata)

        mqttChannel.append(jdata.get('GATEWAY','XX'))
        mqttChannel.append(jdata.get('BUS','YY'))
        mqttChannel.append(str(jdata.get('CAN-ID',None)))
        mqttChannel.append(jdata.get('OBJECT',None))
        mqttChannel.append(jdata.get('METHOD','ZZ'))
        pathindicator = '/'

        publishPath = pathindicator.join(mqttChannel)
        publishPath = '/' + publishPath
        value = jdata.get('VALUE',None)
       # print(gateway)
        #publish = '/OPENHAB'
        print('MEssage', publishPath, value)
        mqtt_data['MESSAGE']= value
        mqtt_data['CHANNEL'] = publishPath
        #mqtt_data['CHANNEL']= self._config.get('PUBLISH')
        print(message)
        msg = 'Received from Socketcan'
        self.msgbus_publish('LOG','%s SocketCanIF: %s MQTT Channel: %s  '%('DEBUG',msg,mqtt_data))

        self.msgbus_publish('MQTT_TX',mqtt_data)



      #  self.start_devices()
