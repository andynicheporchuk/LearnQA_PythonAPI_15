import requests

payload = {"name": "Andrew"}

response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)