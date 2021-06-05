import socket
import time
import json
import threading


ip_server='127.0.0.1'
#ip_server=socket.gethostbyname(socket.gethostname()) - unikamy hardkoding,, gdy wielu klientów
port=2738
#HEADER=255 ???
#FORMAT="utf-8"- ujednolicenie - wpisuję wszedzie FORMAT


MESSAGES=["UPTIME", "INFO", "HELP", "STOP"]
MESSAGES_COMM={"UPTIME":"uptime", "INFO":"info", "HELP":"help", "STOP":"Your connection is closed"}
MESSAGES_COMM["HELP"]=[["UPTIME","cos"], ["INFO", "cos"], ["STOP", "cos"]]


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
server.bind((ip_server, port))
begin=time.time()
begin2=time.ctime(time.time())
print("Czas socketu bind: ", begin2)
print("IP_serwera:", ip_server)

#def client(conn, addres):
    #dla każdego klienta
    #print(f"New coonection {addres}.")
    #connected = True
    #while connected:
    # msg_lenght = conn.recv(HEADER).decode(FORMAT)
    #if msg_lenght:
    # msg_lenght = int(msg_lenght)
    # msg = conn.recv(msg_lenght).decode(FORMAT)
    #print(f"{addres} {msg}")
    #musimy zasygnalizować rozłączenie, by móc ponownie się połączyć
    #jak niżej z message STOP i powinnam conn.close()
    # a gdy chcę, by i serwer coś wysyłał to:
    #conn.send("Msg received".encode(FORMAT))
def client(conn, addres):
    pass

server.listen(10)
while True:
    conn, addres=server.accept()
    #thread = threading.Thread(target=client, args=(conn, addres))
    #thread.start() - gdybyśmy ten start mieli zamknięty w funckji
    #print(f"[aktywne połączenia] {threading.ActiveCount() - 1}")
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
   