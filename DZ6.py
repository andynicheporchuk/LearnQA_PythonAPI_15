import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

count = 0
for i in response.history:
    count += 1

print('Количество редиректов = ', count)

end_url = response.url
print("Конечный URL = ", end_url)

