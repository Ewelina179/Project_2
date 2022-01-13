from dis import show_code
import socket
import json
import time
import threading
import os

from working_with_json import find_user, is_valid_password, read_all_msg, get_names_of_sender, get_messages_of_sender, save_user, check_username_is_exist, save_message, show_users

x=os.path.abspath('server2.py')
print(x)

class User():
    def __init__(self, username):
        self.username = username

    def read(self, conn, end):
        while True:
            type={"message":"Do you want read all mesages or for who?"}
            data=json.dumps(type)
            conn.send(bytes(data, encoding=UTF))
            data = conn.recv(1024)
            data = data.decode(UTF)
            data = json.loads(data) 
            print(data)
            #rozbić na metody
            if data["message"]=="ALL":
                all=read_all_msg(self.username)
                print(all)
                data=json.dumps(all)
                conn.send(bytes(data, encoding=UTF))

            elif data["message"]=="NAME":
                names=get_names_of_sender(self.username)
                print(names)
                lst_names={"names of sender": names}
                data=json.dumps(lst_names)
                conn.send(bytes(data, encoding=UTF))
                data = conn.recv(1024)
                data = data.decode(UTF)
                data = json.loads(data)
                name=data["message"]
                print(name)
                messages=get_messages_of_sender(self.username, name)
                msg = {"messages from sender": messages}
                data = json.dumps(msg)
                conn.send(bytes(data, encoding=UTF))
                next_action = {"message": "Do you want to send another, read or quit?"}
                data = json.dumps(next_action)
                conn.send(bytes(data, encoding=UTF))
                data = conn.recv(256)
                data = data.decode(UTF)
                data = json.loads(data)

                if data["message"] == "READ":
                    self.read(conn)
                elif data["message"] == "SEND":
                    self.send(conn)
                elif data["message"] == "QUIT":
                    x = False
                    get_command(data, end, conn)


    def send(self,conn, end):
        while True:
            users = {"message": show_users()}
            print(users)
            data = json.dumps(users)
            conn.send(bytes(data, encoding=UTF))
            data = conn.recv(1024)
            data = data.decode(UTF)
            data2 = json.loads(data)
            user = data2["message"]
            print(data2["message"])
            print(user)
            message = {"message": "Type message"}
            data = json.dumps(message)
            conn.send(bytes(data, encoding=UTF))
            data = conn.recv(256)
            data = data.decode(UTF)
            data = json.loads(data)
            message_to_save = data["message"]
            print(message_to_save)
            if save_message(self.username, user, message_to_save):
                next_action = {"message": "Message send. Do you want to send another, read or quit?"}
                data = json.dumps(next_action)
                conn.send(bytes(data, encoding=UTF))
                data = conn.recv(256)
                data = data.decode(UTF)
                data = json.loads(data)
                # if read, if send, if quit
            else:
                next_action = {"message": "Message sending failed. Do you want to send another, read or quit?"}
                data = json.dumps(next_action)
                conn.send(bytes(data, encoding=UTF))
                data = conn.recv(256)
                data = data.decode(UTF)
                data = json.loads(data)
                if data["message"] == "READ":
                    self.read(conn)
                elif data["message"] == "SEND":
                    self.send(conn)
                elif data["message"] == "QUIT":
                    x = False
                get_command(data, end, conn)
                
#socket.gethostbyname(socket.gethostname())
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
    else:
        data_to_server=json.dumps(data_to)
        print(data_to)
        conn.send(bytes(data_to_server, encoding=UTF))

def client(conn, address):
    connected=True
    while connected:
        end=time.time()
        end2=time.ctime(end)
        print("Czas połączenia z klientem: ", end2)
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        if data["message"] == "STOP":
            connected = False
        print(data['message'])

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

def stop():
    return {"STOP":"SERVER DISCONNECTION"}

def register(conn):
    type={"message":"REGISTER"}
    data_to_server=json.dumps(type)
    conn.send(bytes(data_to_server, encoding=UTF))
    data = conn.recv(1024)
    data = data.decode(UTF)
    data = json.loads(data)
    username = data["username"]
    if check_username_is_exist(username):
        print(username)
        type = {"message":"Username not exist."}
        data_to_server=json.dumps(type)
        conn.send(bytes(data_to_server, encoding=UTF))
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        password = data["password"]
        print(password)
        save_user(username, password)
        print("good job!")
        type={"message":"OK"}
        data_to_server=json.dumps(type)
        conn.send(bytes(data_to_server, encoding=UTF))
    else:
        type = {"message": "Username already exists!"}
        data_to_server=json.dumps(type)
        conn.send(bytes(data_to_server, encoding=UTF))

def log_in(conn, end):
    while True:
        type = {"message":"LOG IN"}
        data_to_server=json.dumps(type)
        conn.send(bytes(data_to_server, encoding=UTF))
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        username = data["username"]
        print(username)
        x = {"message":"Password"}
        y = {"message":"Invalid login. Try again"}
        if find_user(username):
            data_to_server=json.dumps(x)
            conn.send(bytes(data_to_server, encoding=UTF))
        else:
            data_to_server = json.dumps(y)
            conn.send(bytes(data_to_server, encoding=UTF)) 
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        password = data["password"]
        print(password)
        x = {"message":"You are logged in!"}
        y = {"message": "Invalid password. Try again!"}
        if is_valid_password(username, password):
            data_to_server = json.dumps(x)
            conn.send(bytes(data_to_server, encoding=UTF))
            user = User(username)
            x = {"message": " What do you want to do? READ or SEND - please type one of mentioned or or QUIT to quit user mode."}
            data_to_server = json.dumps(x)
            conn.send(bytes(data_to_server, encoding=UTF))
            data= conn.recv(1024)
            data = data.decode(UTF)
            data = json.loads(data)
            print(data)
            if data["message"] == "READ":
                user.read(conn, end)
            elif data["message"] == "SEND":
                user.send(conn, end)
            elif data["message"] == "QUIT":
                x = False
                get_command(data, end, conn)

if __name__ == "__main__":
    start()
