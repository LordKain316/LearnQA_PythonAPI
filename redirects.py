import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
a = response.history[0]
b = response.history[1]
c = response

print(a.url)
print(b.url)
print(c.url)
