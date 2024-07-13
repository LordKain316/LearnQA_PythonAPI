import requests
import json
import time

a = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parsed = json.loads(a.text)
token = (parsed["token"])
seconds = (parsed["seconds"])
print(token, seconds)

b = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
b1 = b.text   # ложим в переменную текст ответа
x = '{"status":"Job is NOT ready"}'   # объявляем переменную, с ожидаемым значением
if b1 == x:
    time.sleep(seconds)
    c = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
    c1 = c.text   # ложим в переменную текст ответа
    parsed2 = json.loads(c.text)
    result = (parsed2["result"])
    status = (parsed2["status"])
    y = "Job is ready"   # объявляем переменную, с ожидаемым значением
    if status == y and result is not None:
        print("Статус таски верен, поле result в наличии")
    else:
        print("Статус отличается или отсутствует поле result")
else:
    print("Ошибка, задача отработала без параметра token")

