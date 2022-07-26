import requests, time

# создаем задачу, запрос без параметра
response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

# парсим ответ метода
parsed_response1 = response1.json()
token_response1 = parsed_response1["token"]

# перекладываем значение token из ответа в параметр "token"
params = {
    "token": token_response1
}

# перекладываем значение seconds из ответа в переменную sec для time.sleep
sec = parsed_response1["seconds"]

# делаем запрос с параметром "token" сразу после создания задачи
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=params)
parsed_response2 = response2.json()
status = parsed_response2["status"]

# проверяем правильность статуса у неготовой задачи
if status == "Job is NOT ready":
    print("У неготовой задачи статус верный")
else:
    print("Ошибка! Статус неверный у неготовой задачи.")

# ждем кол-во секунд, которое требуется на выполнение задачи
time.sleep(sec)

# делаем запрос после того как задача готова
response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=params)
parsed_response3 = response3.json()
status2 = parsed_response3["status"]

# проверяем правильность статуса и наличие result
if status2 == "Job is ready" and "result" in parsed_response3:
    print("У готовой задачи статус верный, поле result есть в ответе")
else:
    print("Ошибка! У готовой задачи неверный статус или нет поля result.")