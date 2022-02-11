import requests
from lib.base_case import BaseCase


class TestHomeworkHeader(BaseCase):
    def test_homework_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"

        response = requests.get(url)
        print(response.headers)

        homework_header = self.get_header(response, "x-secret-homework-header")
        expected_hw_header_value = "Some secret value"

        assert homework_header == expected_hw_header_value, \
            "Value of the 'x-secret-homework-header' header differs from expected one"
