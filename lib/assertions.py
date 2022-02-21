from requests import Response
import json
import allure


class Assertions:
    @staticmethod
    @allure.step("Check JSON contains {name} = {expected_value}")
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    @allure.step("Check JSON contains key {name}")
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}"

    @staticmethod
    @allure.step("Check status code is {expected_status_code}")
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    @allure.step("Check JSON doesn't contain key {name}")
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name} but it's present"

    @staticmethod
    @allure.step("Check JSON contains the following keys: {names}")
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}"

    @staticmethod
    @allure.step("Check JSON doesn't contain the following keys: {names}")
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}"

        for name in names:
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name} but it's present"

    @staticmethod
    @allure.step("Check the server returns error message '{expected_error_message}'")
    def assert_error_message(response: Response, expected_error_message):
        assert response.content.decode("utf-8") == expected_error_message, \
            f"Unexpected response content {response.content}"
