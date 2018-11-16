import rpyc
from time import time
import logging
import os

INIT_MASTER_LOG = "IP/Port: {}, Time: {}, Tolerance: {}"
CHANGE_TIME_ERROR = "Failed to set time"
CHANGE_TIME_SUCCES = "Succes to set time"
CHANGE_NEW_TIME_ERROR = "Failed to new set time"
CHANGE_NEW_TIME_SUCCES = "Success to new set time"


class Master(object):

    def __init__(self, ip_port, clock_time, logs_file, d, slaves_file):
        self.ip_port = ip_port
        self.clock_time = clock_time
        self.logs_file = logs_file
        self.d = d
        self.ip_list = self.list_ip(slaves_file)
        self.timesum = 0
        self.average = 0
        self.init_master()
        self.clock = time()
        self.set_init_master_time()

    def get_slaves_time(self):
        for ip in self.ip_list:
            try:
                port = int(ip[ip.index(":") + 1:])
                ip_address = ip[:ip.index(":")]
                c = rpyc.connect(ip_address, port)
                difference = c.root.get_time(time())
                if abs(difference) <= self.d*60:
                    self.timesum += difference
                self.createlog("Slave in socket {} connection succeded".format(ip), 'info')
            except ConnectionRefusedError:
                self.createlog("Slave in socket {} not availiable".format(ip), 'error')
                print("Slave in socket {} not availiable".format(ip))

    def calculate_time(self):
        self.average = self.timesum / (len(self.ip_list) + 1)
        print("Time average", str(self.average))
        self.set_master_time()

    def set_init_master_time(self):
        result = os.system("timedatectl set-time '{}'".format(self.clock_time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    def set_master_time(self):
        result = os.system("timedatectl set-time '{}'".format(self.clock_time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    def init_master(self):
        self.createlog(INIT_MASTER_LOG.format(self.ip_port, self.clock_time, self.d), "info")


    @staticmethod
    def list_ip(file_name):

        f = open(file_name, "r")
        ips = f.readlines()
        lista = []
        for ip in ips:
            print(ip)
            lista.append(ip)

        f.close()
        return lista

    def createlog(self, text, l_type):
        logging.basicConfig(filename=self.logs_file, level=logging.INFO)

        if l_type == 'error':
            logging.error(text)
        elif l_type == 'info':
            logging.info(text)
