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

        assert key in response_dict, f"Response JSON doesn't have name' {key}"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code} Actual: {response.status_code}"