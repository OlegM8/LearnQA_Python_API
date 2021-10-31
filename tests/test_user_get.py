import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Get user cases")
class TestUserGet(BaseCase):

    @allure.step("Prepare data for tests")
    def setup(self):
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

    @allure.description("This test checks that only username can be seen without authorization")
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        not_expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, not_expected_fields)

    @allure.description("This test checks that data is received successfully for authorized user ")
    def test_get_user_details_auth_as_same_user(self):

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks that only username can be seen with wrong authorization")
    def test_get_user_details_auth_as_another_user(self):

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        not_expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, not_expected_fields)
