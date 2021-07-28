import socket
import json
from user_classes import User, Admin


UTF="utf-8"

COMM=["UPTIME", "INFO", "HELP", "STOP", "LOG IN", "READ", "SEND", "READ_USER"]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))

class User:
    def __init__(self, name):
        self.name = name
        
    def read(self):
        data = {"message": "READ"}
        data = json.dumps(data)
        client.send(bytes(data,encoding=UTF))
        data=client.recv(1024)
        data = data.decode(UTF)
        print(data)
        answer=input("Type 'ALL' or 'FROM SB'")
        #chyba tu rozbić na metody trzeba
        if answer=="ALL": #uwzględnij małe litery
            data = {"message": "ALL"}
            data = json.dumps(data)
            client.send(bytes(data, encoding=UTF))
        elif answer=="FROM SB":
            data = {"message": "NAME"}
            data = json.dumps(data)
            client.send(bytes(data, encoding=UTF))
            data=client.recv(1024)
            data = data.decode(UTF)
            #data = json.loads(data)
            print(data)
            from_who=input("Type name of sender")
            data = {"message": from_who}
            data = json.dumps(data)
            client.send(bytes(data, encoding=UTF))
            data = client.recv(1024)
            data = data.decode(UTF)
            data = json.loads(data)
            print(data)

        else:
            print("Try again")
            #tu musi cofnąć do pytania - answer, w razie co
        data=client.recv(1024)
        #data = json.loads(data)
        data = data.decode(UTF)
        print(data)

    def send(self):
        data = {"message": "SEND"}
        data = json.dumps(data)
        client.send(bytes(data, encoding=UTF))
        data = client.recv(1024)
        data = data.decode(UTF)
        print(data)
        question=input("Who do you want to send message?")
        data = {"message": question}
        data = json.dumps(data)
        client.send(bytes(data, encoding=UTF))
        data = client.recv(1024)
        data = data.decode(UTF)
        print(data)
        question2 = input("Type message")
        data = {"message": question2}
        data = json.dumps(data)
        client.send(bytes(data, encoding=UTF))
        data = client.recv(1024)
        data = data.decode(UTF)
        print(data)#jeszcze nie napisałam tej części po stronie serwera
#może przenieść. porozbijać na pliki.
class Admin(User):
    def init(self, name):
        self.name = name

    def read_user():
        pass#czyta od kogo chce wiadomości

    #def read_user_all():
    #    pass#czyta wszystkie usera


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
    username=input("Please enter your login ;p: ")
    print(username)
    user_data={}
    user_data["username"]=username
    data = json.dumps(user_data)
    client.send(bytes(data,encoding=UTF))
    data=client.recv(1024)
    data = data.decode(UTF)
    
    print(data)
    print(type(data))
    print(data[-10:-2])
    if data[-10:-2]=="Password":
        password=input("Please enter your password: ")
        print(password)
        user_data={}
        user_data["password"]=password
        data = json.dumps(user_data)
        client.send(bytes(data,encoding=UTF))
        data=client.recv(1024)
        data = data.decode(UTF)
        #A MOŻE BY TAK JSON LOADS?????????????
        print(data[-12:-2])
        if data[-12:-2]=="logged in!":
            if username=="Admin": #też zawrzeć, że dowolna litera
                user=Admin(username)
                print("Admin logged in!")#potem się tym zajmę
            else:
                user=User(username)
                print("User logged in!")
                data = client.recv(1024)
                data = data.decode(UTF)
                print(data)
                answer=input("READ or SEND?: ")
                if answer == "READ": #uwzględniać małe litery
                    user.read()
                elif answer == "SEND":
                    user.send()
                
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

