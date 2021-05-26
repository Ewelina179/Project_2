import socket
import time
import threading
import json

ip_server='127.0.0.1'
port=2738
HEADER = 64
FORMAT = 'utf-8'

MESSAGES=["UPTIME", "INFO", "HELP", "STOP"]
MESSAGES_COMM={"UPTIME":"uptime", "INFO":"info", "HELP":"help", "STOP":"Your connection is closed"}
MESSAGES_COMM["HELP"]=[["UPTIME","cos"], ["INFO", "cos"], ["STOP", "cos"]]
#t = time.localtime()
#print "time.asctime(t): %s " % time.asctime(t)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.bind((ip_server, port))
    begin=time.time()
    begin2=time.ctime(time.time())
    print("Czas socketu bind: ", begin2)
    print("IP_serwera:", ip_server)
    s.listen(10)
    conn, addres=s.accept()
    with conn: 
        end=time.time()
        end2=time.ctime(time.time())
        print ('Klient z adresu', addres)
        print("Czas połączenia z klientem: ", end2)
        while True:

            uptime_value={}
            uptime=end-begin
            MESSAGES_COMM["UPTIME"]=uptime
            info={}
            info["server version number"]="jeszcze nie wiem"
            info["data utworzenia"] = begin2
            MESSAGES_COMM["INFO"]=info

            data = conn.recv(1024)
            data = data.decode("utf-8")
            data=json.loads(data)
            print(data)
            print(data['message'])
            for x in range(len(MESSAGES)):
                
                if MESSAGES[x] == data['message']:
                    y=data['message']
                    print(MESSAGES_COMM[y])
                    data_to_server=json.dumps(MESSAGES_COMM[y])
                    conn.send(bytes(data_to_server, encoding="utf-8"))
                elif MESSAGES[x] == "STOP":
                    conn.close()
            conn.sendall(bytes(data_to_server,encoding="utf-8"))

#	client.send(time.ctime(time.time())) # wyslanie danych do klienta
#wrzuć to w loop!
"""
if data["message"] == "INFO":
                data3=json.dumps(info)
                conn.send(bytes(data3, encoding="utf-8"))
            if data["message"] == "HELP":
                data4=json.dumps(help)
                conn.send(bytes(data4, encoding="utf-8"))
                """