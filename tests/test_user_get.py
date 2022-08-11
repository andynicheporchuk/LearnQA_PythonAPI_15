import requests
from lib.base_case import BaseCase
from lib.assertions import Assertion

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertion.assert_json_has_key(response,"username")
        Assertion.assert_json_has_not_key(response,"firstName")
        Assertion.assert_json_has_not_key(response,"email")
        Assertion.assert_json_has_not_key(response,"lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_login = self.get_json_value(response1, "user_id")


        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_login}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username","email", "firstName", "lastName"]

        Assertion.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_other_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")


        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/3}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid}
        )

        unexpected_fields = ["email", "firstName", "lastName"]

        Assertion.assert_status_code(response2, 404)

        Assertion.assert_json_has_key(response2, "username")
        Assertion.assert_json_has_not_keys(response2, unexpected_fields)


