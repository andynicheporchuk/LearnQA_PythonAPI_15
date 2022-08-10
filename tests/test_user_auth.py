import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertion

class TestUserAuth(BaseCase):
    params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data = data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_login = self.get_json_value(response1, "user_id")

    def test_auth_user(self):

        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid": self.auth_sid }
        )

        Assertion.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_login,
            "User id from login method is not equal to user id from check method"
        )


    @pytest.mark.parametrize('status', params)

    def test_negative_auth_user(self, status):

        if status == "no_cookie":
            response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":self.token}
            )

        else:
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid }
            )

        Assertion.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f'User is authorized with status {status}'
        )










