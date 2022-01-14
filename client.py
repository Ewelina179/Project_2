import socket
import json
from user_classes import User


UTF = "utf-8"

COMM = ("UPTIME", "INFO", "HELP", "STOP", "LOG IN", "REGISTER", "READ", "SEND", "READ_USER")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))

class User:
    def __init__(self, name):
        self.name = name
        
    def read(self):
        data = {"message": "READ"}
        send(data)
        data = receive()
        print(data)
        answer=input("Type 'ALL' or 'FROM SB' or QUIT to quit log in mode")
        if answer == "ALL":
            data = {"message": "ALL"}
            send(data)
        elif answer == "FROM SB":
            data = {"message": "NAME"}
            send(data)
            data = receive()
            print(data)
            from_who=input("Type name of sender")
            data = {"message": from_who}
            send(data)
            data = receive_loads()
            print(data)
        elif answer == "QUIT":
            data = {"message": "QUIT"}
            send(data)
            start()
        else:
            print("Try again")
        data = receive()
        print(data)

    def send(self):
        while True:
            data = {"message": "SEND"}
            send(data)
            data = receive_loads()
            users = data["message"]
            question = input(f"Who do you want to send message? List of users: {users}. Type QUIT if want to quit log in mode.")
            data = {"message": question}
            if question == "QUIT":
                send(data)
                start()
            else:
                send(data)
                receive_loads()
                message = input("Type message max 255 signs")
                data = {"message": message}
                send(data)
                receive_loads()

    
def client_send(y):
    data = {}
    for x in range(len(COMM)): 
        if COMM[x] == y:
            data["message"] = y
            data = json.dumps(data)
            client.sendall(bytes(data,encoding=UTF))
            data = receive_loads()
            print(repr(data))
            if repr(data) == {"message": "LOG IN"}:
                log_in()
            if repr(data) == {"message": "REGISTER"}:
                print("tuuu")
                register()

def start():
    print('You can choose command from list. Type {} to get information about commands.'.format(COMM[2]))
    while True:
        answer = input()
        print(answer)
        client_send(answer)
        if answer =="LOG IN":
            log_in()
        elif answer =="REGISTER":
            register()
        elif answer =="STOP":
            close_msg = {}
            close_msg["message"] = "STOP"
            send(close_msg)
            client.close()
            break
        else:
            client_send(answer)

def register():
    username=input("Please type your username ;p: ")
    print(username)
    user_data = {}
    user_data["username"] = username
    send(user_data)
    data = receive_loads()
    print(data)
    if data == {"message":"Username already exists!"}:
        print("Registration failed. Try again!")
    elif data == {"message":"Username not exist."}:
        password = input("Please enter your password: ")
        user_data = {}
        user_data["password"] = password
        send(data)
        data = receive_loads(data)
        print(data)
        if data == {"message": "OK"}:
            print(data)
            print("You are able to login. Type command LOG IN")
        else:
            print(data)
            print("Registration failed. Try again!")

def log_in():
    username = input("Please enter your login ;p: ")
    print(username)
    user_data = {}
    user_data["username"] = username
    send(user_data)
    data = receive() 
    print(data)
    print(type(data))
    print(data[-10:-2])
    if data[-10:-2] == "Password":
        password=input("Please enter your password: ")
        print(password)
        user_data={}
        user_data["password"] = password
        send(user_data)
        data = receive()
        print(data[-12:-2])
        if data[-12:-2] == "logged in!":
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
            elif answer == "QUIT":
                data = {"message": "QUIT"}
                send(data)
                start()      
        else:
            print("Invalid password! Try again!") # zrobić, żeby nie wywalało na początek
    else:
        print("Invalid username! Try again!")

def send(data):
    data = json.dumps(data)
    client.send(bytes(data, encoding=UTF))

def receive():
    data = client.recv(1024)
    data = data.decode(UTF)
    return data

def receive_loads():
    data = client.recv(1024)
    data = data.decode(UTF)
    data = json.loads(data)
    return data

if __name__ == "__main__":
    start()