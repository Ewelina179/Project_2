import json

def find_user(username):
    with open('users.json') as j:
        data=json.load(j)
    return any(username==subvalue["username"] for subvalue in data["users"])

def is_valid_password(username, password):
    with open('users.json') as j:
        data=json.load(j)
        for x in data["users"]:
            if username==x["username"]:
                return password==x["password"]

x=find_user("Ewelina")
print(x)
y=is_valid_password("Ewelina", "Ewelina12")
print(y)