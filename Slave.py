import rpyc
from time import time
import logging
import os

TIME_EVENT = "Get time event "
SLAVE_CURRENT_TIME = "Slave current time {}"
CHANGE_TIME_ERROR = "Failed to set time"
CHANGE_TIME_SUCCES = "Success to set time"


class Slave(rpyc.Service):

    def __init__(self, ip_port, clock_time, logs_file):
        self.ip_port = ip_port
        self.clock_time = clock_time
        self.logs_file = logs_file

    def exposed_get_time(self, master_time):
        print(TIME_EVENT)
        self.createlog(TIME_EVENT, "info")
        current_time = SLAVE_CURRENT_TIME.format(str(time()))
        print(current_time)
        self.createlog(current_time, "info")

        difference = master_time - time()
        self.createlog(TIME_EVENT, 'info')
        return difference

    def set_slave_time(self):
        result = os.system("timedatectl set-time '{}'".format(self.clock_time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    '''def exposed_set_time(self, new_time):
        os.system("timedatectl set-time '{}'".format(self.clock_time))'''

    def createlog(self, text, l_type):
        logging.basicConfig(filename=self.logs_file, level=logging.INFO)

        if l_type == 'error':
            logging.error(text)
        elif l_type == 'info':
            logging.info(text)
