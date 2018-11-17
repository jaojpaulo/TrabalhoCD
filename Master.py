import rpyc
from datetime import datetime
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
        self.agents_count = 0
        self.init_master()
        self.set_init_master_time()

    def get_slaves_time(self):
        self.agents_count = len(self.ip_list) + 1
        for ip in self.ip_list:
            try:
                port = int(ip[ip.index(":") + 1:])
                ip_address = ip[:ip.index(":")]
                c = rpyc.connect(ip_address, port)
                time_s = self.parse_time()
                difference = c.root.get_time(time_s)
                if abs(difference) <= self.d*60:
                    self.timesum += difference
                else:
                    self.agents_count -= 1
                self.createlog("Slave in socket {} connection succeded".format(ip), 'info')
            except ConnectionRefusedError:
                self.agents_count -= 1
                self.createlog("Slave in socket {} not availiable".format(ip), 'error')
                print("Slave in socket {} not availiable".format(ip))

    def calculate_time(self):
        self.average = self.timesum / (len(self.ip_list) + 1)
        print("Time average", str(self.average))
        self.set_machines_time()

    def set_init_master_time(self):
        hours = "00"
        minutes = "00"
        seconds = "00"
        time_m = 0
        time_h = 0
        if self.average > 59:
            time_m = int(self.average/60)
            seconds = str(self.average - (time_m*60))
        if time_m > 59:
            time_h = int(time_m/60)
            minutes = str(time_m - (time_h*60))
        if time_h > 0:
            hours = str(time_h)
        time_f = hours+":"+minutes+":"+seconds
        print(time_f)
        result = os.system("timedatectl set-time '{}'".format(time_f))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")
            return time_f

    def init_master(self):
        self.createlog(INIT_MASTER_LOG.format(self.ip_port, self.clock_time, self.d), "info")

    def parse_time(self):
        t = datetime.now()
        return (t.hour*3600) + (t.minute*60) + t.second

    def set_machines_time(self):
        time_f = self.set_init_master_time()
        for ip in self.ip_list:
            try:
                port = int(ip[ip.index(":") + 1:])
                ip_address = ip[:ip.index(":")]
                c = rpyc.connect(ip_address, port)
                c.root.set_time(time_f)
                self.createlog("Slave in socket {} connection succeeded".format(ip), 'info')
            except ConnectionRefusedError:
                self.agents_count -= 1
                self.createlog("Slave in socket {} not available".format(ip), 'error')
                print("Slave in socket {} not available".format(ip))

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
