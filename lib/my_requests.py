import requests
import allure
from envirnoment import ENV_OBJECT



class MyRequests():
    # публичные методы
    #
    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, params, headers, cookies, 'GET')

    @staticmethod
    def post(url:str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url,data,headers,cookies, 'POST')

    @staticmethod
    def put(url:str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url,data,headers,cookies, 'PUT')

    @staticmethod
    def delete(url:str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url,data,headers,cookies, 'DELETE')



    @staticmethod
    # _send - приватный метод, которая не должна использоваться извне
    def _send(url:str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        # выбираем метод с которым будет запущен тест

        if method == 'GET':
            response = requests.get(url,params=data, headers = headers, cookies = cookies)
        elif method == 'POST':
            response = requests.post(url,data=data, headers = headers, cookies = cookies)
        elif method == 'PUT':
            response = requests.put(url,data=data, headers = headers, cookies = cookies)
        elif method == 'DELETE':
            response = requests.delete(url,data=data, headers = headers, cookies = cookies)
        else:
            raise Exception(f"Bad http method {method} was recieved")

        # возвращаем значение во внешнюю часть программы
        return response
