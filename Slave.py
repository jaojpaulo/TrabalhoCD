import rpyc
from datetime import datetime
import logging
import os

INIT_SLAVE_LOG = "IP/Port: {}, Time: {}"
TIME_EVENT = "Get time event "
SLAVE_CURRENT_TIME = "Slave current time {}"
CHANGE_TIME_ERROR = "Failed to set time"
CHANGE_TIME_SUCCES = "Success to set time"
CHANGE_NEW_TIME_ERROR = "Failed to new set time"
CHANGE_NEW_TIME_SUCCES = "Success to new set time"


class Slave(rpyc.Service):

    def __init__(self, ip_port, clock_time, logs_file):
        self.ip_port = ip_port
        self.clock_time = clock_time
        self.logs_file = logs_file
        self.init_slave()
        self.set_init_slave_time()

    def exposed_get_time(self, master_time):
        print(TIME_EVENT)
        self.createlog(TIME_EVENT, "info")
        current_time = SLAVE_CURRENT_TIME.format(str(datetime.now()))
        print(current_time)
        self.createlog(current_time, "info")

        difference = master_time - self.parse_time()
        self.createlog(TIME_EVENT, 'info')
        return difference

    def exposed_set_time(self, new_time):
        result = os.system("timedatectl set-time '{}'".format(new_time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    def set_init_slave_time(self):
        result = os.system("timedatectl set-time '{}'".format(self.clock_time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    def init_slave(self):
        self.createlog(INIT_SLAVE_LOG.format(self.ip_port, self.clock_time), "info")

    def parse_time(self):
        t = datetime.now()
        return (t.hour * 3600) + (t.minute * 60) + t.second

    def createlog(self, text, l_type):
        logging.basicConfig(filename=self.logs_file, level=logging.INFO)

        if l_type == 'error':
            logging.error(text)
        elif l_type == 'info':
            logging.info(text)
