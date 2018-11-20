import rpyc
from datetime import datetime, timedelta
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

        current_time = datetime.now()
        print(SLAVE_CURRENT_TIME.format(str(current_time.hour+":"+current_time.minute+":"+current_time.second)))
        time_d = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
        self.createlog(SLAVE_CURRENT_TIME.format(str(current_time.hour+":"+current_time.minute+":"+current_time.second)), "info")

        difference = master_time - time_d
        self.createlog(TIME_EVENT, 'info')
        return int(difference.total_seconds())

    def exposed_set_time(self, new_time):
        correct_time_msg = "Correct time {}".format(new_time.decode("utf-8"))
        print(correct_time_msg)
        self.createlog(correct_time_msg, "info")
        result = os.system("timedatectl set-time '{}'".format(new_time.decode("utf-8")))
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
