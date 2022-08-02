import requests, pytest

class TestAPI:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers)

        # assert "HomeWork" in response.cookies, 'Response has not "HomeWork" in cookie'