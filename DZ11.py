import requests, pytest

class TestAPI:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        print(response.cookies)
        actual_cookie = response.cookies["HomeWork"]

        assert "HomeWork" in response.cookies, 'Response has not "HomeWork" in cookie'
        assert "hw_value" == actual_cookie, 'Response has Error cookie'
