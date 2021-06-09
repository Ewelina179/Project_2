import socket
import json
import time
import threading

#socket.gethostbyname(socket.gethostname())
IP_SERVER="127.0.0.1"
PORT=2738
UTF="utf-8"
VERSION_OF_SERVER=112

MESSAGES={"UPTIME":"TIME OF CONNECTION WITH CLIENT APPLICATION", "INFO":"SERVER VERSION NUMBER, DATE OF SERVER CREATION(???)", "HELP":{"LIST OF AVAILABLE COMMANDS":{"UPTIME":"cos", "INFO":"cos", "STOP":"cos", "LOG IN":"wez z wyzej"}}, "STOP":"SERVER DISCONNECTION", "LOG IN":"LOG IN AND GET ACCESS TO PERSONAL DATA"}


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
        
        print ('Klient z adresu', address)
        
        thread=threading.Thread(target=client, args=(conn, address))
        thread.start()

def client(conn, address):
    connected=True
    while connected:
        end=time.time()
        end2=time.ctime(end)
        print("Czas połączenia z klientem: ", end2)
        data = conn.recv(1024)
        data = data.decode(UTF)
        data = json.loads(data)
        print(data)
        print(data['message'])
        
        a=data['message']
        func= {
            "INFO": info(begin2),
            "UPTIME": uptime(end, begin),
            "HELP": help()
            
        }
        data_to=func.get(a)
        data_to_server=json.dumps(data_to)
        print(data_to)
        conn.send(bytes(data_to_server, encoding=UTF))    
        #plus handle default
            
def uptime(end, begin):
    uptime_value={}
    uptime=end-begin
    MESSAGES["UPTIME"]=uptime
    return MESSAGES.fromkeys(["UPTIME"], uptime)

def info(begin2):
    info={}
    info["SERVER VERSION NUMBER"]=VERSION_OF_SERVER
    info["DATE OF SERVER CREATION"] = begin2
    MESSAGES["INFO"]=info
    return MESSAGES.fromkeys(["INFO"], info)
     
#help wysyła bez "help:"". ale chyba może być
def help():
    return MESSAGES["HELP"]["LIST OF AVAILABLE COMMANDS"]

def stop():
    return {"STOP":"SERVER DISCONNECTION"}

def log_in():
    pass
#na komendę log in i login sprawdz czy jest i odpowiedz adekwatnie
#jak zwrotnie poda hasło to zaloguj - stworz obiekt ktory dziala na swoich zasobach wg zasad z klasy

def receive_msg():
    pass

def lst_of_msg():
    pass

def logout():
    pass



if __name__=="__main__":
    start()


#na zaś - pewnie porozbijać na pliki
#testy integracyjne też do tego???

#klasa user? odczytaj komunikat i wyciagnij adekwatne dane i odeslij. gdy przyjdzie do zapisu (bo ktos wyslal) i przekroczy 5 to komunikat
#klasa admin moze ze wszystkich czytac i zmieniac haslo (chyba tez)
#zwykly user czyta tylko swoje wiadomosci i swoje danie zmienia
#odbijanie piłeczki z serwerem na poziomie klasy
