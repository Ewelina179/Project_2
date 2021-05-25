import socket
import time
import threading
import json

ip_server='127.0.0.1'
port=2738
HEADER = 64
FORMAT = 'utf-8'

UPTIME_MESSAGE="UPTIME"
INFO_MESSAGE = "INFO"
HELP_MESSAGE = "HELP"
DISCONNECT_MESSAGE = "STOP"

#t = time.localtime()
#print "time.asctime(t): %s " % time.asctime(t)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.bind((ip_server, port))
    begin=time.time()
    print("Czas socketu bind: ", begin)
    print("IP_serwera:", ip_server)
    s.listen(10)
    conn, addres=s.accept()
    with conn: 
        end=time.time()
        print ('Klient z adresu', addres)
        print("Czas połączenia z klientem: ", end)
        while True:
            uptime=end-begin
            data = conn.recv(1024)
            if not data:
                break
            elif data=="uptime":
                conn.send(uptime)
            conn.sendall(data)
"""
while 1:
	client,addr = s.accept() # odebranie polaczenia
	print 'Polaczenie z ', addr
	client.send(time.ctime(time.time())) # wyslanie danych do klienta
	client.close()
"""