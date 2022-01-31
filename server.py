import socket
import json
import time
import threading
import os

from working_with_json import find_user, is_valid_password, read_all_msg, get_names_of_sender, get_messages_of_sender, save_user, check_username_is_exist, save_message, show_users

from user import User

x=os.path.abspath('server.py')

IP_SERVER = "127.0.0.1"
PORT = 2738
UTF = "utf-8"
VERSION_OF_SERVER = "0.1.0"

MESSAGES = {
    "UPTIME":"TIME OF CONNECTION WITH CLIENT APPLICATION",
    "INFO":"SERVER VERSION NUMBER, DATE OF SERVER CREATION(???)",
    "HELP":{
        "LIST OF AVAILABLE COMMANDS":{
            "UPTIME":"TIME OF CONNECTION WITH CLIENT APPLICATION",
            "INFO":"SERVER VERSION NUMBER, DATE OF SERVER CREATION(???)",
            "STOP":"SERVER DISCONNECTION",
            "LOG IN":"LOG IN AND GET ACCESS TO PERSONAL DATA",
            "REGISTER": "REGISTER USER"}},
    "STOP":"SERVER DISCONNECTION",
    "REGISTER": "REGISTER USER",
    "LOG IN":"LOG IN AND GET ACCESS TO PERSONAL DATA",
    "READ":"READ YOUR MESSAGES, IF LOGGED IN",
    "SEND": "SEND MESSAGES TO OTHERS USERS, IF YOU ARE LOGGED IN",
    }


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_SERVER, PORT))

begin=time.time()
begin2=time.ctime(begin)

print("Connection time", begin2)
print("Server IP address:", IP_SERVER)

def start():
    server.listen()
    while True:
        conn, address = server.accept()
        
        print('Klient z adresu', address)
        
        thread=threading.Thread(target=client, args=(conn, address))
        thread.start()

        if conn:
            break

def get_command(data, end, conn):
    a = data['message']
    print("takie to")
    print(data)
    func= {
        "INFO": info(begin2),
        "UPTIME": uptime(end, begin),
        "HELP": help(),
        "STOP": stop()
    }
    data_to=func.get(a)
    if a == "LOG IN":
        log_in(conn, end)
    elif a == "REGISTER":
        register(conn)
    elif a == "QUIT":
        quit(data, end, conn)
    else:
        data_to_server=json.dumps(data_to)
        conn.send(bytes(data_to_server, encoding=UTF))

def client(conn, address):
    connected=True
    while connected:
        end=time.time()
        end2=time.ctime(end)
        print("Czas połączenia z klientem: ", end2)
        data = receive_loads(conn)
        if data["message"] == "STOP":
            connected = False
        get_command(data, end, conn)
            
def uptime(end, begin):
    uptime_value={}
    uptime=end-begin
    MESSAGES["UPTIME"]=uptime
    return MESSAGES.fromkeys(["UPTIME"], uptime)

def info(begin2):
    info = {}
    info["SERVER VERSION NUMBER"] = VERSION_OF_SERVER
    info["DATE OF SERVER CREATION"] = begin2
    MESSAGES["INFO"] = info
    return MESSAGES.fromkeys(["INFO"], info)
     
def help():
    return MESSAGES["HELP"]["LIST OF AVAILABLE COMMANDS"]

def close(conn):
    stop()
    conn.close()

def quit(data, end, conn):
    get_command(data, end, conn)

def stop():
    return {"STOP":"SERVER DISCONNECTION"}

def register(conn):
    type={"message": "REGISTER"}
    send(conn, type)
    data = receive_loads(conn)
    username = data["username"]
    if check_username_is_exist(username):
        type = {"message":"Username not exist."}
        send(conn, type)
        data = receive_loads()
        password = data["password"]
        save_user(username, password)
        type={"message":"OK"}
        send(conn, type)
    else:
        type = {"message": "Username already exists!"}
        send(conn, type)

def log_in(conn, end):
        type = {"message":"LOG IN"}
        send(conn, type)
        data = receive_loads(conn)
        username = data["username"]
        x = {"message":"Password"}
        y = {"message":"Invalid login. Try again"}
        if find_user(username):
            send(conn, x)
        else:
            send(conn, y)
        data = receive_loads(conn)
        password = data["password"]
        x = {"message":"You are logged in!"}
        y = {"message": "Invalid password. Try again!"}
        if is_valid_password(username, password):
            send(conn, x)
            user = User(username)
            x = {"message": " What do you want to do? READ or SEND - please type one of mentioned or or QUIT to quit user mode."}
            send(conn, y)
            data = receive_loads(conn)
        while True:
            if data["message"] == "READ":
                user.read(conn, end)
                continue
            elif data["message"] == "SEND":
                user.send(conn, end)
                continue
            elif data["message"] == "QUIT":
                data = receive_loads(conn)
                get_command(data, end, conn)
            else:
                data = receive_loads(conn)
                get_command(data, end, conn)


def send(conn, message):
    data = json.dumps(message)
    conn.send(bytes(data, encoding=UTF))

def receive(conn):
    data = conn.recv(1024)
    data = data.decode(UTF)
    return data

def receive_loads(conn):
    data = conn.recv(1024)
    data = data.decode(UTF)
    data = json.loads(data)
    return data

if __name__ == "__main__":
    start()
