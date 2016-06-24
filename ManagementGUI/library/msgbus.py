__author__ = 'oper'

class msgbus1(object):
    callerList = {}

    def __init__(self):
        test =0
        print('msgbus')


    def msgbus_subscribe(self, channel, callback):

        if channel not in msgbus1.callerList.keys():
   #         print ('Create Channel new')
            msgbus1.callerList[channel] = []
        msgbus1.callerList[channel].append(callback)

   #     print('callerList',msgbus.callerList)

        return True

    def unsubscribe(self, channel, callback):

        if channel in msgbus1.callerList.keys():
            msgbus1.callerList[channel].remove(callback)

        return True

    def unsubscribe_all(self, channel):

        if channel in msgbus1.callerList.keys():
            msgbus1.callerList[channel] = []

        return True

    def has_subscriber(self,channel):

        result = 0

        if channel in msgbus1.callerList.keys():
            result = len(msgbus1.callerList[channel])

        return result

    def msgbus_publish(self, channel, *args, **kwargs):

        result = False

    #   print('Hier',channel)
        if channel in msgbus1.callerList.keys():
            result = True
     #       print('Channel',channel)
            for item in msgbus1.callerList[channel]:
         #       print('Item',channel,item)
                item(*args, **kwargs)
        else:
            print('Channel not found')

        return result

    def debug(self):

        print ('DEBUG',msgbus1.callerList)

        return

