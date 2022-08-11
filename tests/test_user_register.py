import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertion
from datetime import datetime

class TestUserRegister(BaseCase):

    # варианты с отсутствием одного из полей
    data = [
        ({"firstName": "learnqa","lastName": "learnqa","email": "testmail@example.com","password": "123"}),
        ({"username": "testuser","lastName": "learnqa","email": "testmail@example.com","password": "123"}),
        ({"username": "testuser","firstName": "learnqa","email": "testmail@example.com","password": "123"}),
        ({"username": "testuser","firstName": "learnqa","lastName": "learnqa","password": "123"}),
        ({"username": "testuser","firstName": "learnqa","lastName": "learnqa","email": "testmail@example.com"}),
    ]

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime('%m%d%y%H%M%S')
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email,
            "password": "123"
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
            response,
            200
        )

        Assertion.assert_json_has_key(
            response,
            "id"
        )


    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email,
            "password": "123"
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
            response,
            400
        )

        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('data', data)

    # Создание пользователя без указания одного из полей
    def test_create_user_without_required_field(self, data):

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
           response,
           400
        )

        if "username" not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: username", f"Unexpected response content {response.content}"
        elif "firstName" not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: firstName", f"Unexpected response content {response.content}"
        elif "lastName" not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: lastName", f"Unexpected response content {response.content}"
        elif "email" not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: email", f"Unexpected response content {response.content}"
        elif "password" not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: password", f"Unexpected response content {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_with_wrong_email(self):
        email = "testmailexample.ru"
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email,
            "password": "123"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
            response,
            400
        )

        # проверяем, получаем ли мы тот текст ошибки, который ожидаем
        assert response.content.decode("utf-8") == 'Invalid email format', f"Unexpected response content {response.content}"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_name(self):
        data = {
            "username": "learnqa",
            "firstName": "l",
            "lastName": "learnqa",
            "email": self.email,
            "password": "123"
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
            response,
            400
        )

        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", f"Unexpected response content {response.content}"


    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        data = {
            "username": "learnqa",
            "firstName": "cfceezjoewecfrfbuckxanrvzpyerakzplmxqhyluqidwjndsiybyccuquaddfkzmibxhpiroxbxxqlonqollaxdbxedzfuxhufvgrqwwytludolgmuwfxjqtfdmijoyhejialkkusvufoijosfzqdbvtllgyaraolxlduptpvmdgmffbmnlqxsdhjndgwzlpqssroasotjoughovdxxsjbrbcktkaxfbbaesbyqcdmgvujcfjdqsmladbasdffghjkl",
            "lastName": "learnqa",
            "email": self.email,
            "password": "123"
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertion.assert_status_code(
            response,
            400
        )

        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", f"Unexpected response content {response.content}"




