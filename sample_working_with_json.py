import json
import os

x=os.path.abspath('users.json')
print(x)

def find_user(username):
    x=os.path.abspath('users.json')
    with open(x) as j:
        data=json.load(j)
    return any(username==subvalue["username"] for subvalue in data["users"])

#wyżej filter(lambda)???
# coś w ten, że user=next(filter(lambda x: x["username"]==username, data["users"]), None)

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
        #polskie znaki?

def get_names_of_sender(username):
    with open('messages.json') as m:
        data = json.load(m)
        for x in data["users"]:
            if username==x["username"]:
                names=[]
                for el in x["messages from"]: #.keys
                    name=[x for x in el.keys()]
                    names.append(name)
            return names

""""
x=find_user("Ewelina")
print(x)
y=is_valid_password("Ewelina", "Ewelina12")
print(y)
"""
