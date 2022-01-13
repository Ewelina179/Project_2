import json
import os


def check_username_is_exist(username):
    with open('users.json', "r") as j:
        file = json.load(j)
        return False if any(username==subvalue["username"] for subvalue in file["users"]) else True

def create_inbox(username):
    with open('messages.json', "r") as j:
        file = json.load(j)
    with open('messages.json', "w") as j:
        file["users"].append({"username": username, "messages from": []})
        json.dump(file, j)

def save_user(username, password):
    new_user = {"username": username, "password": password}
    with open('users.json', "r") as j:
        file = json.load(j)
    with open('users.json', "w") as j:
        file["users"].append(new_user)
        json.dump(file, j)
    create_inbox(username)


def find_user(username):
    x=os.path.abspath('users.json')
    with open(x) as j:
        data=json.load(j)
    return any(username==subvalue["username"] for subvalue in data["users"])

def is_valid_password(username, password):
    with open('users.json') as j:
        data=json.load(j)
        for x in data["users"]:
            if username==x["username"]:
                return password==x["password"]

def read_all_msg(username):
    with open('messages.json') as m:
        data = json.load(m)
        for x in data["users"]:
            if username==x["username"]:
                all_msg=x["messages from"]
                return all_msg

def get_names_of_sender(username):
    with open('messages.json') as m:
        data = json.load(m)
        for x in data["users"]:
            if username==x["username"]:
                names=[]
                for el in x["messages from"]:
                    name=[x for x in el.keys()]
                    names.append(name)
            return names

def get_messages_of_sender(username, name):
    with open('messages.json') as m:
        data = json.load(m)
        for x in data["users"]:
            if username==x["username"]:
                msg=[]
                for el in x["messages from"]:
                    for key, value in el.items():
                        if key==name:
                            message = value
                            msg.append(message)
                return msg

def show_users():
    with open('messages.json') as j:
        file = json.load(j)
        return [x["username"] for x in file["users"]]


def save_message(username, user, message):
    with open('messages.json') as j:
        file = json.load(j)
        a = [x for x in file["users"] if x["username"] == user][0]
        if a:
            b = a["messages from"]
            el = {}
            el[username] = message
            b.append(el)
            with open('messages.json', 'w') as j:
                json.dump(file, j)
                return True
        else:
            return False