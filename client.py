import socket
import json

from user_client import User

UTF = "utf-8"

COMM = ("UPTIME", "INFO", "HELP", "STOP", "LOG IN", "REGISTER", "READ", "SEND", "READ_USER")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2738))
    
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
                register()

def start():
    print('You can choose command from list. Type {} to get information about commands.'.format(COMM[2]))
    while True:
        answer = input()
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
    user_data = {}
    user_data["username"] = username
    send(user_data)
    data = receive_loads()
    if data == {"message":"Username already exists!"}:
        print("Registration failed. Try again!")
    elif data == {"message":"Username not exist."}:
        password = input("Please enter your password: ")
        user_data = {}
        user_data["password"] = password
        send(data)
        data = receive_loads(data)
        if data == {"message": "OK"}:
            print("You are able to login. Type command LOG IN")
        else:
            print("Registration failed. Try again!")

def log_in():
    username = input("Please enter your login ;p: ")
    user_data = {}
    user_data["username"] = username
    send(user_data)
    data = receive()
    if data[-10:-2] == "Password":
        password=input("Please enter your password: ")
        user_data={}
        user_data["password"] = password
        send(user_data)
        data = receive()
        if data[-12:-2] == "logged in!":
            user=User(username)
            print("User logged in!")
            data = client.recv(1024)
            data = data.decode(UTF)
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
            print("Invalid password! Try again!")
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