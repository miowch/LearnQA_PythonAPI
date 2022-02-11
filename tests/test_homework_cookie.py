import requests
from lib.base_case import BaseCase


class TestHomeworkCookie(BaseCase):
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url)
        print(response.cookies)

        homework_cookie = self.get_cookie(response, "HomeWork")
        expected_hw_cookie_value = "hw_value"

        assert homework_cookie == expected_hw_cookie_value, "Value of HomeWork cookie differs from expected one"
