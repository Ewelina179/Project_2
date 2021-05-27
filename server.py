import socket
import time
import json

ip_server='127.0.0.1'
port=2738


MESSAGES=["UPTIME", "INFO", "HELP", "STOP"]
MESSAGES_COMM={"UPTIME":"uptime", "INFO":"info", "HELP":"help", "STOP":"Your connection is closed"}
MESSAGES_COMM["HELP"]=[["UPTIME","cos"], ["INFO", "cos"], ["STOP", "cos"]]


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
server.bind((ip_server, port))
begin=time.time()
begin2=time.ctime(time.time())
print("Czas socketu bind: ", begin2)
print("IP_serwera:", ip_server)
server.listen(10)
while True:
    conn, addres=server.accept()
    connected = True
    while connected:
        end=time.time()
        end2=time.ctime(time.time())
        print ('Klient z adresu', addres)
        print("Czas połączenia z klientem: ", end2)
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
                connected=False
   