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
