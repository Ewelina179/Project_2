import socket
import json
import time
import threading

IP_SERVER=socket.gethostbyname(socket.gethostname())
PORT=5431
UTF="utf-8"
VERSION_OF_SERVER=112

"""
MESSAGES=["UPTIME", "INFO", "HELP", "STOP"]
MESSAGES={"UPTIME":"uptime", "INFO":"info", "HELP":"help", "STOP":"Your connection is closed"}
MESSAGES["HELP"]=[["UPTIME","cos"], ["INFO", "cos"], ["STOP", "cos"]]
"""
MESSAGES={"UPTIME":"TIME OF CONNECTION WITH CLIENT APPLICATION", "INFO":"SERVER VERSION NUMBER, DATE OF SERVER CREATION(???)", "HELP":"LIST OF AVAILABLE COMMAND", "STOP":"SERVER DISCONNECTION"}

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_SERVER, PORT))

begin=time.time()
begin2=time.ctime(begin)

print("Czas połączenia", begin2)
print("Adres IP serwera:", IP_SERVER)
d={}
#a=[MESSAGES.items() for MESSAGES if MESSAGES.key()=="INFO"]
a=MESSAGES.fromkeys(["HELP"], "a")
print(a)

def start():
    server.listen()
    while True:
        conn, address = server.accept()
        end=time.time()
        end2=time.ctime(end)
        print ('Klient z adresu', address)
        print("Czas połączenia z klientem: ", end2)
        thread=threading.Thread(target=client, arg=(conn, address))
        thread.start()

def client(conn, address):
    connected=True
    while connected:
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        print(data)
        print(data['message'])
        """
        for x in range(len(MESSAGES)):
                
            if MESSAGES[x] == data['message']:
                y=data['message']
                print(MESSAGES_COMM[y])
                data_to_server=json.dumps(MESSAGES_COMM[y])
                conn.send(bytes(data_to_server, encoding="utf-8"))
            elif MESSAGES[x] == "STOP":
                connected=False
            """
        # to rozwiązanie wyżej godzi w naturę słowników ;p
        for key in MESSAGES.keys():
            if data['message']=="UPTIME":
                data_to=uptime()
            elif data['message']=="INFO":
                data_to=info()
            elif data['message']=="HELP":
                data_to=help() 
            elif data['message']=="STOP":
                connected=False
            data_to_server=json.dumps(data_to)
            print(data_to)
            conn.send(bytes(data_to_server, encoding="utf-8"))            
#czy jeszcze jedna funckja json dumps + send??? i wywowałać wewnątrz?
#zwróć uwagę czy tak powinno być z tym json-ami
#tutaj wszystko aż do conn.send() - chyba....

#nie wiem czy tak nazywać funkcję "client"...
#i tu jeśli msg taka a taka to odpal fukncję np. uptime
def uptime(end, begin):
    uptime_value={}
    uptime=end-begin
    MESSAGES["UPTIME"]=uptime
    return MESSAGES.fromkeys(["UPTIME"], uptime)

def info(begin2):
    info={}
    info["SERVER VERSION NUMBER"]=VERSION_OF_SERVER
    info["DATE OF SERVER CREATION"] = begin2
    MESSAGES["INFO"]=info
    return MESSAGES.fromkeys(["INFO"], info)
     
#help ma dać listę komend!
def help():
    return MESSAGES

def stop():
    pass

def log_in():
    pass

def receive_msg():
    pass

def lst_of_msg():
    pass

def logout():
    pass



print(info(begin2))
print(help())