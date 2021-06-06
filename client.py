import socket
import json


UTF="utf-8"

COMM=["UPTIME", "INFO", "HELP", "STOP"]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))
"""
def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    a teraz dotarło echo:
    print(client.recv(2048).decode(FORMAT) - duży skrót - większa liczba, żeby nie tym samym portem(???)
"""

def client_send(y):
    data ={}
    for x in range(len(COMM)):   
        if COMM[x]==y:
            data["message"]=y
            data = json.dumps(data)
            client.sendall(bytes(data,encoding=UTF))
            data=client.recv(1024)
            data = data.decode(UTF)
            print(repr(data))
#czy ta funckja nie powinna być jeszcze pokrojona? i chyba tu już kwestia testów integracyjnych

def start():
    print('You can choose command from list. Type {} to get information about commands.'.format(COMM[2]))
    while True:
        z=input()
        client_send(z)
        if z=="STOP":
            client.close()
            break

start()

"""
if __name__=="__main__":
    start()
"""

