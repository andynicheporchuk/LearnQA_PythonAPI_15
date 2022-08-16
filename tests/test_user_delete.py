import requests
from lib.assertions import Assertion
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure

@allure.epic("User cases")
class TestUserDelete(BaseCase):

    @allure.description("Удаление пользователя с id 2")
    @allure.feature("Действия над пользователями")
    @allure.story("Удаления пользователя")
    @allure.severity("minor")

    # удалить пользователя по ID 2
    def test_delete_user_with_id_2(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Заменям запись на MyRequests.post("/user/login", data)
        # response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        response1 = MyRequests.post("/user/login", data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        with allure.step(f"ШАГ ПОСЛЕ POST. куки =  {auth_sid}"):
           pass


        # DELETE
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertion.assert_status_code(response2, 400)

        assert response2.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', f"Unexpected response, maybe user deleted"



    @allure.description("Удаление пользователя, из-под которого авторизован")
    @allure.feature("Действия над пользователями")
    @allure.story("Удаления пользователя")
    @allure.severity("trivial")

    #  удалить пользователя, из-под которого авторизован
    def test_delete_user_auth_same_user(self):
        # CREATE
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            "email": email,
            "password": password
        }

        # LOGIN

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_login = self.get_json_value(response2, "user_id")


        # DELETE

        response3 = MyRequests.delete(
            f"/user/{user_id_from_login}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )


        Assertion.assert_status_code(response3, 200)


        # GET

        response4 = MyRequests.get(
            f"/user/{user_id_from_login}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )


        Assertion.assert_status_code(response4, 404)

        assert response4.text == 'User not found', f"User with id {user_id_from_login} hasn't been deleted"

    @allure.description("Удаление пользователя, будучи авторизованными другим пользователем")
    @allure.feature("Действия над пользователями")
    @allure.story("Удаления пользователя")
    @allure.severity("critical")
    # удалить пользователя, будучи авторизованными другим пользователем
    def test_delete_user_auth_other_user(self):

        # REGISTER - Регистрация пользователя
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        email = register_data["email"]
        password = register_data["password"]

        login_data = {
            "email": email,
            "password": password
        }

        # LOGIN

        response = MyRequests.post("/user/login", data=login_data)


        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")


        # DELETE

        other_user_id = 41609

        response2 = MyRequests.delete(
            f"/user/{other_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # GET

        response3 = MyRequests.get(
            f"/user/{other_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertion.assert_status_code(response3, 200)

        assert "username" in response3.text, f"User with id = {other_user_id} deleted"


