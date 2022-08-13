import requests
from lib.base_case import BaseCase
from lib.assertions import Assertion

class TestUserEdit(BaseCase):
    def setup(self):
        # REGISTER - Регистрация пользователя
        register_data = self.prepare_registration_data()

        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertion.assert_status_code(response1, 200)
        Assertion.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.password = register_data["password"]
        self.firstName = register_data["firstName"]
        self.user_id = self.get_json_value(response1, "id")

        self.login_data = {
            "email": self.email,
            "password": self.password
        }

        # LOGIN

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")


    def test_edit_just_created_user(self):

        # LOGIN - Авторизация пользователя

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # EDIT - Изменение данных авторизованного пользователя

        new_firstName = 'Changed name'

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid},
            data = {"firstName": new_firstName}
        )

        Assertion.assert_status_code(response3, 200)


        # GET- Получение измененных данных авторизованного пользователя

        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid}
        )

        Assertion.assert_status_code(response4, 200)

        Assertion.assert_json_value_by_name(
            response4,
            "firstName",
            new_firstName,
            f"Wrong firstName of user after edit"
        )

    # Негативные тесты

    # изменить данные пользователя, будучи неавторизованными
    def test_edit_user_details_not_auth_user(self):
        # EDIT
        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            data={"firstName": "new name"}
        )

        Assertion.assert_status_code(response, 400)

        assert response.content.decode("utf-8") == 'Auth token not supplied', f"Unexpected response content = {response.content}"


    # изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_details_auth_other_user(self):

        # EDIT
        response2 = requests.put(
            f"https://playground.learnqa.ru/api/user/10",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": "new name 1"}
        )

        # GET
        response3 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertion.assert_json_value_by_name(response3, "firstName", "new name", f"The data of the user with id = {self.user_id} has changed. The method PUT does not work correctly, data was requested by id = 10.")


    # изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_email_to_invalid_auth_same_user(self):

        # EDIT
        response2 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": "testmailexample.ru"}
        )

        Assertion.assert_status_code(response2, 400)

        assert response2.content.decode("utf-8") == 'Invalid email format',f"Unexpected response content = {response2.content}"


    # изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_firstName_to_short_auth_same_user(self):
        # EDIT
        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": "q"}
        )

        Assertion.assert_status_code(response, 400)

        assert response.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', f"Unexpected response content = {response.content}"







