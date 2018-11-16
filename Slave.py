import rpyc
from time import time
import logging
import os


class Slave(rpyc.Service):

    def __init__(self, ip_port, clock_time, logs_file):
        self.ip_port = ip_port
        self.clock_time = clock_time
        self.logs_file = logs_file

    def exposed_get_time(self, master_time):
        print("Get time event ")
        print("Time 1", str(time()))
        #print("Time 2", str(self.time))
        difference = master_time - time()
        self.createlog("Get time event", 'info')
        return difference

    def set_slave_time(self):
        os.system("date +%T -s '{}'".format(self.clock_time))

    '''def exposed_set_time(self, new_time):
        os.system()'''

    def createlog(self, text, l_type):
        logging.basicConfig(filename=self.logs_file, level=logging.INFO)

        if l_type == 'error':
            logging.error(text)
        elif l_type == 'info':
            logging.info(text)
