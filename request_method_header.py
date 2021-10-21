import requests


class TestMethodHeader:
    def test_method_header(self):
        request_url = "https://playground.learnqa.ru/api/homework_header"

        response = requests.get(request_url)
        print(response.headers)

        assert response.headers.get("x-secret-homework-header") == "Some secret value", \
            "The cookie value is not 'Some secret value'"
