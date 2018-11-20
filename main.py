from Master import Master
from Slave import Slave
import time
import fire


class Machine(object):

    def Machine(self, mtype, ip_port, clock_time, logs_file, **kwargs):
        i = 0
        if mtype is 'm':
            master = Master(ip_port, clock_time, logs_file, kwargs['d'], kwargs['slaves_file'])
            while True:
                i += 1
                print("Execution ", i)
                master.get_slaves_time()
                master.calculate_time()
                time.sleep(5)

        elif mtype is 's':
            slave = Slave(ip_port, clock_time, logs_file)
            from rpyc.utils.server import ThreadedServer
            print("Slave machine")
            t = ThreadedServer(slave, port=int(ip_port[ip_port.index(':')+1:]))
            t.start()
        else:
            print("Option not available")


if __name__ == '__main__':
    fire.Fire(Machine)



