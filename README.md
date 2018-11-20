# TrabalhoCD
Trabalho de computação distribuída sobre o algoritmo de Berkeley

Ambiente
Para executar a aplicação é necessário instalar as packages fire e rpcy via pip:

    pip install fire
    pip install rpyc

O projeto é composto do por três arquivos python, 'main.py' responsável por instanciar as chamadas das clases reponsáveis por implementar 
as funções utilizadas para cada uma das classes que reprsentam os dois possíveis perfis de máquina, Slave(Slave.py) ou Master(Master.py).
O arquivo 'iplist.txt' lista os conjunto ip:porta para cada máquina do tipo slave que a máquina master irá se conectar. A pasta persiste
contem os arquivos de log para a máquina slave(logfiles.log) ou master(logfielm.log) onde são aramzandas a informaçãoes de log.

Após a instalação, rodar a plicação de acordo com o os comandos  

Para Master:
    Machine --mtype m --ip-port localhost:18861 --clock-time 10:16:05 --logs-file persist/logfilem.log --d 20 --slaves-file iplist.txt

Para Slave:
    Machine --mtype s --ip-port localhost:18861 --clock-time 10:16:05 --logs-file persist/logfiles.log