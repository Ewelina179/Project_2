import socket
import json
from user_classes import User, Admin


UTF="utf-8"

COMM=["UPTIME", "INFO", "HELP", "STOP", "LOG IN"]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))


def client_send(y):
    data ={}
    for x in range(len(COMM)):
       # if COMM[x]=="LOG IN":
        #    log_in()   
        if COMM[x]==y:
            data["message"]=y
            data = json.dumps(data)
            client.sendall(bytes(data,encoding=UTF))
            #data=client.recv(1024)
            #data = data.decode(UTF)
            #print(repr(data))
#czy ta funckja nie powinna być jeszcze pokrojona? i chyba tu już kwestia testów integracyjnych

def start():
    print('You can choose command from list. Type {} to get information about commands.'.format(COMM[2]))
    while True:
        z=input()
        client_send(z)
        if z=="LOG IN":
            log_in()
            
        elif z=="STOP":
            client.close()
            break
        else:
            client_send(z)#problem z pozostałymi komendami, poza log in, bo tracą "łącze" z serwerem


def log_in():
    #stąd czeka na info od serwera i wysyła username
    data=client.recv(1024)
    data = data.decode(UTF)
    #print(repr(data))
    username=input("Please again ;p: ")
    print(username)
    user_data={}
    user_data["username"]=username
    data = json.dumps(user_data)
    client.send(bytes(data,encoding=UTF))
    data=client.recv(1024)
    if data["answer"]==True:
        password=input('Please enter your password: ')
        user_data={}
        user_data["password"]=password
        data = json.dumps(user_data)
        client.send(bytes(data,encoding=UTF))
        user_data.client.recv(1024)
        if user_data["answer"]==True:
            if username=="Admin": #też zawrzeć, że dowolna litera
                user=Admin(username)
                print("Admin logged in!")
            else:
                user=User(username)
                print("User logged in!")
        else:
            print("Invalid password! Try again!") # zrobić, żeby nie wywalało na początek
    else:
        print("Invalid username! Try again!")

def log_out():
    pass
    #nie wie, czy wylogowanie nie bedzie w user klasie



start()

"""
if __name__=="__main__":
    start()
"""

