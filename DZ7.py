import requests

type_requests = ["GET", "POST", "PUT", "DELETE"]

response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response1.text)

response2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response2.text)

response3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params = {"method": "GET"})
print(response3.text)

for i in type_requests:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": i})
    print("Запрос на метод GET c параметром method = %s, Ответ = " % (i), response.text)
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Запрос на метод POST c параметром method = %s, Ответ = " % (i), response.text)
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Запрос на метод PUT c параметром method = %s, Ответ = " % (i), response.text)
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Запрос на метод DELETE c параметром method = %s, Ответ = " % (i), response.text)