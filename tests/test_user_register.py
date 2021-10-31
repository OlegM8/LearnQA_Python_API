import requests
import pytest
import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):

    data = ([
        [{'password': '', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',
          'email': "123456@example.com"}, 'password'],
        [{'password': '123', 'username': '', 'firstName': 'learnqa', 'lastName': 'learnqa',
          'email': "123456@example.com"}, 'username'],
        [{'password': '123', 'username': 'learnqa', 'firstName': '', 'lastName': 'learnqa',
          'email': "123456@example.com"}, 'firstName'],
        [{'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': '',
          'email': "123456@example.com"}, 'lastName'],
        [{'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName':
            'learnqa', 'email': ""}, 'email']
    ])

    @allure.description("This test checks successful user registration")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.description("This test checks that user with already existing email can't be registered")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("This test checks that user with incorrect email format can't be registered")
    def test_create_user_with_invalid_email_format(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Email format is valid"

    @allure.description("This test checks that user can't be registered without any of required fields")
    @pytest.mark.parametrize('data', data)
    def test_create_user_without_one_field(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data[0])

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{data[1]}' field is too short", \
            f"All data is valid"

    @allure.description("This test checks that user with too short name can't be registered")
    def test_create_user_with_too_short_name(self):
        data = self.prepare_registration_data(username='l')

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The value of 'username' field has correct length"

    @allure.description("This test checks that user with too long name can't be registered")
    def test_create_user_with_too_long_name(self):
        data = self.prepare_registration_data(username='l' * 251)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"The value of 'username' field has correct length"
