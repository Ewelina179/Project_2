import socket
import json

from working_with_json import read_all_msg, get_names_of_sender, get_messages_of_sender, save_message, show_users

from server import send, receive_loads, get_command


class User():

    def __init__(self, username):
        self.username = username

    def read(self, conn, end):
        while True:
            type = {"message": "Do you want to read messages from everyone or from a selected user?"}
            send(conn, type)
            data = receive_loads(conn)
            if data["message"]=="ALL":
                all = read_all_msg(self.username)
                send(conn, all)
                continue
            elif data["message"]=="NAME":
                names=get_names_of_sender(self.username)
                lst_names={"names of sender": names}
                send(conn, data)
                data = receive_loads(conn)
                name=data["message"]
                messages=get_messages_of_sender(self.username, name)
                msg = {"messages from sender": messages}
                send(conn, msg)
                next_action = {"message": "Do you want to send another, read or quit?"}
                send(conn, next_action)
                data = receive_loads(conn)
                continue
            elif data["message"] == "QUIT":
                data = receive_loads(conn)
                get_command(data, end, conn)
            else:
                data = receive_loads(conn)
                get_command(data, end, conn)

    def send(self,conn, end):
        while True:
            users = {"message": show_users()}
            send(conn, users)
            data = receive_loads(conn)
            user = data["message"]
            message = {"message": "Type message"}
            send(conn, message)
            data = receive_loads(conn)
            message_to_save = data["message"]
            if save_message(self.username, user, message_to_save):
                next_action = {"message": "Message sent. Do you want to send another, read or quit?"}
                send(conn, next_action)
                data = receive_loads(conn)
                if data["message"] == "READ":
                    self.read(conn)
                elif data["message"] == "SEND":
                    self.send(conn, end)
                elif data["message"] == "QUIT":
                    data = receive_loads(conn)
                    get_command(data, end, conn)
                else:
                    data = receive_loads(conn)
                    get_command(data, end, conn)
            else:
                next_action = {"message": "Message sending failed. Do you want to send another, read or quit?"}
                send(conn, next_action)
                data = receive_loads(conn)
                if data["message"] == "READ":
                    self.read(conn)
                elif data["message"] == "SEND":
                    self.send(conn)
                elif data["message"] == "QUIT":
                    data = receive_loads(conn)
                    get_command(data, end, conn)
                else:
                    data = receive_loads(conn)
                    get_command(data, end, conn)