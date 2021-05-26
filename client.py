import socket
import sys
import json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

UPTIME_MESSAGE="UPTIME"
INFO_MESSAGE = "INFO"
HELP_MESSAGE = "HELP"
DISCONNECT_MESSAGE = "STOP"
COMM=["UPTIME", "INFO", "HELP", "STOP"]
#SERVER = socket.gethostbyname(socket.gethostname())
#ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))



#data = json.dumps(j)
"""
    s.sendall(bytes(data,encoding="utf-8"))
    a = s.recv(1024)
    a = a.decode("utf-8")
    print ('Json: ', repr(a))

"""
def send_uptime(y):
    data ={}
    for x in range(len(COMM)):
        if COMM[x]==y:
            data["message"]=y
            data2 = json.dumps(data)
            #print(data2)
            client.sendall(bytes(data2,encoding="utf-8"))
            data=client.recv(1024)
            data = data.decode("utf-8")
            print('JSON:', repr(data))

    
send_uptime("UPTIME")
send_uptime("INFO")
send_uptime("STOP")