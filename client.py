import socket
import sys
import json

j = {"name": "Olek", "surname": "Nowak"} 


data = json.dumps(j)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 2738))
    s.sendall(bytes(data,encoding="utf-8"))
    a = s.recv(1024)
    a = a.decode("utf-8")
    print ('Json: ', repr(a))
    
    