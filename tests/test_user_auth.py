import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):

    @allure.step("Get data for authorization")
    def setup(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        request_url = "https://playground.learnqa.ru/api/user/login"
        response = requests.post(request_url, data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

    @allure.description("This test successfully authorises as correct user")
    def test_user_auth(self):

        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method != user id from check method")
