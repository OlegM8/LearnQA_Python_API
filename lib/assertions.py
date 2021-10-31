from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response:Response, name, expected_value, error_message):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert name in response_dict, f"Response JSON doesn't have name' {name}"
        assert response_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response:Response, key):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert key in response_dict, f"Response JSON doesn't have name' {key}."

    @staticmethod
    def assert_json_has_keys(response: Response, keys: list):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        for key in keys:
            assert key in response_dict, f"Response JSON doesn't have name' {key}."

    @staticmethod
    def assert_json_has_not_key(response: Response, key):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert key not in response_dict, f"Response JSON shouldn't have name' {key}. But it's present."

    @staticmethod
    def assert_json_has_not_keys(response: Response, keys: list):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        for key in keys:
            assert key not in response_dict, f"Response JSON should't have name' {key}. But it's present."

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code} Actual: {response.status_code}"

    @staticmethod
    def assert_response_text(response: Response, text):
        assert response.text == text, f"Wrong response text. Expected: {text} Actual: {response.text}"
