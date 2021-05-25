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

DIC={"message":"UPTIME", "INFO_MESSAGE":"INFO"}
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
            uptime_value={}
            uptime=end-begin
            uptime_value["Czas"]=uptime
            info={}
            info["server version number"]="jeszcze nie wiem"
            data = conn.recv(1024)
            data = data.decode("utf-8")
            data=json.loads(data)
            if data["message"] == "UPTIME":
                data2=json.dumps(uptime_value)
                conn.send(bytes(data2, encoding="utf-8"))
            if data["message"] == "INFO":
                data3=json.dumps(info)
                conn.send(bytes(data3, encoding="utf-8"))
            if data["message"] == "STOP":
                break
            #conn.sendall(bytes(data2,encoding="utf-8"))#conn.send(data2)

#	client.send(time.ctime(time.time())) # wyslanie danych do klienta
#wrzuć to w loop!