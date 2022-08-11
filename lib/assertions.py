from requests import Response
import json

class Assertion:
    # класс - родитель, и чтобы вызывать метод без создания объекта нужно сделать staticmethod
    @staticmethod
    # убеждаемся что значение внутри json доступно по опред. имени и равно тому, чему мы ожидали
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON has not key {name}"

        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON has not key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        for name in names:
            assert name in response_as_dict, f"Response JSON has not key {name}"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        for name in names:
            assert name in response_as_dict, f"Response JSON shouldn't has key {name}, but it's present."




    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Unexpected status code {response.status_code}. Expected status code = {expected_status_code}"


    @staticmethod

    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        assert name not in response_as_dict, f"Response JSON shouldn't has key {name}, but it's present."
