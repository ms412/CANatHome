import logging
import logging.handlers
import socket


class logger(object):

    def __init__(self,name,syslogHost):

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        hostname = socket.gethostname()
        formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s'.format(hostname),'%b %e %H:%M:%S')

        handler = logging.handlers.SysLogHandler(address=(syslogHost, 514), facility=19)
        handler.setFormatter(formatter)

        self._logger.addHandler(handler)

    def debug(self,msg):
        self._logger.debug(msg)

    def info(self,msg):
        self._logger.info(msg)

    def critical(self,msg):
        self._logger.critical(msg)

class app(object):

    def __init__(self,log):
        self._log = log
        self._log.info('start')

    def methode(self, x):
        msg = 'test' + x
        self._log.debug(msg)


if __name__ == '__main__':
    log = logger('TEST', '172.17.115.215')
    log.info('TEST')
    appX = app(log)
    appX.methode('iii')

