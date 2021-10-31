import json.decoder
import requests
import allure
from requests import Response
from datetime import datetime
from lib.assertions import Assertions


class BaseCase:

    @allure.step("Get cookie")
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"No cookie {cookie_name} in the last response"
        return response.cookies[cookie_name]

    @allure.step("Get header")
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"No header {headers_name} in the last response"
        return response.headers[headers_name]

    @allure.step("Get json value")
    def get_json_value(self, response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert name in response_dict, f"Response JSON doesn't have name' {name}"

        return response_dict[name]

    @allure.step("Get json value")
    def prepare_registration_data(self, email=None, username=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        if username is None:
            username = 'learnqa'

        return {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    @allure.step("Register new user")
    def register_new_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        return email, first_name, password, user_id

    @allure.step("Login as a user")
    def login(self, email, password):
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        return auth_sid, token