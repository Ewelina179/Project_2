import json

f=open('users.json')
data=json.load(f)
#c to dane, które przyszły
c="Ewelina"
x=data["users"][1]["username"]
y=data["users"]
is_name=any(c==subvalue["username"] for subvalue in data["users"])
print(x)
print(y)
print(is_name)
f.close()
#jeśli True to adekwatny komunikat itd., żeby podał hasło dla tego imienia
#teraz sprawdź czy hasło jest dla tego imienia konkretnego!
d="Ewelina12"
is_password=[d==subvalue["password"] for subvalue in data["users"] if subvalue["username"]==c]
print(is_password)
#działa. tylko ten generator ogarnij
#jeśli drugie to true to tworzę konkretny obiekt+wysyłam komunikat, że zalogowano. czy źle? czy to w komunkacie od klienta za każdym razem, że zalogowany??????????????