import requests

print("Hello from Максим")

a = requests.get("https://playground.learnqa.ru/api/get_text")
print(a.text)