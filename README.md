# TrabalhoCD
Trabalho de computação distribuída sobre o algoritmo de Berkeley

Para executar a aplicação é necessário instalar as packages fire e rpcy via pip:

    pip install fire
    pip install rpyc

Após a instalação, rodar a plicação de acordo com o os comandos  

Para Master:
    Machine --mtype m --ip-port localhost:18861 --clock-time 10:16:05 --logs-file persist/logfilem.log --d 20 --slaves-file iplist.txt

Para Slave:
    Machine --mtype s --ip-port localhost:18861 --clock-time 10:16:05 --logs-file persist/logfiles.log