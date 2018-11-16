import rpyc
from time import time
import logging
import os


class Master(object):

    def __init__(self, ip_port, clock_time, logs_file, d, slaves_file):
        self.ip_port = ip_port
        self.clock_time = clock_time
        self.logs_file = logs_file
        self.d = d
        self.ip_list = self.list_ip(slaves_file)
        self.timesum = 0
        self.average = 0
        self.clock = time()
        self.set_master_time()

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

    def set_master_time(self):
        os.system("date +%T -s '{}'".format(self.clock_time))

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
