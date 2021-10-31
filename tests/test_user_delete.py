import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Delete cases")
class TestUserDelete(BaseCase):

    @allure.step("Register and login new user")
    def setup(self):
        # REGISTER
        self.email, self.first_name, self.password, self.user_id = self.register_new_user()

        # LOGIN
        self.auth_sid, self.token = self.login(self.email, self.password)

    @allure.description("This test checks that protected user can't be deleted")
    def test_delete_protected_user(self):
        auth_sid, token = self.login('vinkotov@example.com', '1234')

        response = requests.delete("https://playground.learnqa.ru/api/user/2",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test checks successfully delete the new user")
    def test_delete_user(self):
        # DELETE
        response1 = requests.delete(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response1, 200)

        # GET
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response2, 404)
        Assertions.assert_response_text(response2, "User not found")

    @allure.description("This test checks that user can't be deleted with wrong authorization")
    def test_delete_user_wrong_authorization(self):
        # User1 is registered in setup method, then register user2 and try to delete user1
        # using auth_sid and token for user2

        # REGISTER
        email2, first_name2, password2, user_id2 = self.register_new_user()

        # LOGIN
        auth_sid2, token2 = self.login(email2, password2)

        # DELETE
        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                    headers={"x-csrf-token": token2},
                                    cookies={"auth_sid": auth_sid2})

        Assertions.assert_status_code(response2, 400)
