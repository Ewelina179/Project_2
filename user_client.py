from client import send, receive_loads, receive, start

class User:
    def __init__(self, name):
        self.name = name
        
    def read(self):
        data = {"message": "READ"}
        send(data)
        data = receive()
        answer=input("Type 'ALL' or 'FROM SB' or QUIT to quit log in mode")
        if answer == "ALL":
            data = {"message": "ALL"}
            send(data)
        elif answer == "FROM SB":
            data = {"message": "NAME"}
            send(data)
            data = receive()
            from_who=input("Type name of sender")
            data = {"message": from_who}
            send(data)
            data = receive_loads()
        elif answer == "QUIT":
            data = {"message": "QUIT"}
            send(data)
            start()
        else:
            print("Try again")
        data = receive()

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