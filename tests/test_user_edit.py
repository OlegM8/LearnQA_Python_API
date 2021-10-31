import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Edit cases")
class TestUserEdit(BaseCase):

    @allure.step("Register and login new user")
    def setup(self):
        # REGISTER
        self.email, self.first_name, self.password, self.user_id = self.register_new_user()

        # LOGIN
        self.auth_sid, self.token = self.login(self.email, self.password)

    @allure.description("This test edit created new user")
    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Changed name"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            "Changed name",
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks that user can't be edited without authorization")
    def test_edit_user_without_authorization(self):
        new_name = "Changed name"

        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                data={"firstName": new_name})

        Assertions.assert_response_text(response, "Auth token not supplied")
        Assertions.assert_status_code(response, 400)

    @allure.description("This test checks that user can't be edited with wrong authorization")
    def test_edit_user_with_wrong_authorization(self):
        # Register the new user1 in setup() method, then register user2, login as user2 and try to edit user1
        # but using token and auth_sid from user2

        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email2 = register_data['email']
        password2 = register_data['password']

        # LOGIN
        login_data = {
            'email': email2,
            'password': password2
        }

        request_url = "https://playground.learnqa.ru/api/user/login"
        response2 = requests.post(request_url, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": auth_sid},
                                 cookies={"auth_sid": token},
                                 data={"firstName": new_name})

        Assertions.assert_response_text(response3, "Auth token not supplied")
        Assertions.assert_status_code(response3, 400)

    @allure.description("This test checks that email can't be changed to incorrect format")
    def test_edit_user_incorrect_format(self):
        # EDIT
        new_email = "textincorrectformatexample.com"

        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                headers={"x-csrf-token": self.token},
                                cookies={"auth_sid": self.auth_sid},
                                data={"email": new_email})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    @allure.description("This test checks that firstname can't be changed to too short name")
    def test_edit_user_too_short_first_name(self):
        # EDIT
        new_name = "1"

        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                headers={"x-csrf-token": self.token},
                                cookies={"auth_sid": self.auth_sid},
                                data={"firstName": new_name})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_name(
            response, "error", "Too short value for field firstName", "The name 1 character long shouldn't be allowed")
