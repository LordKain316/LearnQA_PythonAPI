import requests

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"HEAD"})
print(response.text)
print(response.status_code)

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"POST"})
print(response.text)
print(response.status_code)


parameters_methods_list = [{"method":"GET"}, {"method":"POST"}, {"method":"PUT"}, {"method":"DELETE"}]

for param in parameters_methods_list:
        result = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
        print(f"метод GET с параметром params={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"метод GET с параметром data={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"метод POST с параметром data={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
        print(f"метод POST с параметром params ={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"метод PUT с параметром data={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
        print(f"метод PUT с параметром params ={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"метод DELETE с параметром data={param} выдал следующий результат {result.text} со status_code {result.status_code}")
        result = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
        print(f"метод DELETE с параметром params ={param} выдал следующий результат {result.text} со status_code {result.status_code}")