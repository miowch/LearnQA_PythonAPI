import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    @allure.step("Log in as test user and get authentication data")
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User gets authenticated by email and password")
    @allure.description("This test successfully authorises user by email and password")
    def test_auth_user(self):
        with allure.step("Get ID of authorised user"):
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )

        with allure.step("Check that returned user ID equals ID of authorised user"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                self.user_id_from_auth_method,
                "User ID from auth method is not equal to user id from check method"
            )

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User cannot get authorisation status with {condition}")
    @allure.description("This test checks authorisation status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        with allure.step("Try to get ID of authorised user with {condition} in request"):
            if condition == "no_cookie":
                response2 = MyRequests.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token}
                )
            else:
                response2 = MyRequests.get(
                    "/user/auth",
                    cookies={"auth_sid": self.auth_sid}
                )
        with allure.step("Check that 0 gets returned instead of user ID"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                0,
                f"User is authorized with condition {condition}"
            )
