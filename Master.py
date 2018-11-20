import rpyc
from datetime import datetime, timedelta
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
        self.init_master_log()
        self.set_init_master_time()

    def get_slaves_time(self):
        self.agents_count = len(self.ip_list) + 1
        for ip in self.ip_list:
            try:
                port = int(ip[ip.index(":") + 1:])
                ip_address = ip[:ip.index(":")]
                c = rpyc.connect(ip_address, port,)
                current_t = datetime.now()
                print("Currente Master time {}:{}:{}".format(str(current_t.hour),str(current_t.minute),str(current_t.second)))
                time_d = timedelta(hours=current_t.hour,minutes=current_t.minute, seconds=current_t.second)
                difference = c.root.get_time(time_d)
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
        print("Time average {} seconds".format(str(self.average)))
        self.set_machines_time()

    def set_machines_time(self):
        time_f = self.set_master_time()
        for ip in self.ip_list:
            try:
                port = int(ip[ip.index(":") + 1:])
                ip_address = ip[:ip.index(":")]
                c = rpyc.connect(ip_address, port)
                c.root.set_time(time_f)
                self.createlog("Slave in socket {} connection succeeded".format(ip), 'info')
            except ConnectionRefusedError:
                self.agents_count -= 1
                self.createlog("Slave in socket {} not available for time update".format(ip), 'error')
                print("Slave in socket {} not available for time update".format(ip))

    def set_master_time(self):
        seconds_f = self.average % 60
        minute_intermediari = int(self.average/60)
        minutes_f = minute_intermediari % 60
        hour_f = int(minute_intermediari/60)

        cur_time = timedelta(hours=datetime.now().hour,minutes=datetime.now().minute, seconds=datetime.now().second)

        avg_time = timedelta(hours=hour_f, minutes=minutes_f, seconds=seconds_f)
        final = cur_time + avg_time
        self.set_init_master_time(time=str(final))
        return str(final)

    def set_init_master_time(self, time=None):
        if not time:
            time = self.clock_time
        result = os.system("timedatectl set-time '{}'".format(time))
        if result == 256:
            self.createlog(CHANGE_TIME_ERROR, "error")
        else:
            self.createlog(CHANGE_TIME_SUCCES, "info")

    def init_master_log(self):
        self.createlog(INIT_MASTER_LOG.format(self.ip_port, self.clock_time, self.d), "info")

    def parse_time(self):
        t = datetime.now()
        return (t.hour*3600) + (t.minute*60) + t.second


    @staticmethod
    def list_ip(file_name):

        f = open(file_name, "r")
        ips = f.readlines()
        lista = []
        for ip in ips:
            lista.append(ip)

        f.close()
        return lista

    def createlog(self, text, l_type):
        logging.basicConfig(filename=self.logs_file, level=logging.INFO)

        if l_type == 'error':
            logging.error(text)
        elif l_type == 'info':
            logging.info(text)
