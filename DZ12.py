import requests, pytest

class TestAPI:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers)
        actual_header = response.headers.get("x-secret-homework-header")

        assert "x-secret-homework-header" in response.headers, 'Response has not "x-secret-homework-header" in headers'
        assert actual_header == "Some secret value", 'Response has error header "x-secret-homework-header"'