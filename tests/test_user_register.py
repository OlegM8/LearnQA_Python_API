import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


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

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_invalid_email_format(self):
        email = "vinkotovexample.com"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format: '{email}'", \
            f"Email format is valid"

    @pytest.mark.parametrize('data', data)
    def test_create_user_without_one_field(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data[0])

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{data[1]}' field is too short", \
            f"All data is valid"

    def test_create_user_with_too_short_name(self):
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The value of 'username' field has correct length"

    def test_create_user_with_too_long_name(self):
        data = {
            'password': '123',
            'username': 'l' * 251,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"The value of 'username' field has correct length"
