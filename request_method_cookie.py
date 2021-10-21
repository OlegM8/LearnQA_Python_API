import requests


class TestMethodCookies:
    def test_method_cookie(self):
        request_url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(request_url)
        print(response.cookies)

        assert response.cookies.get("HomeWork") == "hw_value", "The cookie value is not 'hw_value'"
