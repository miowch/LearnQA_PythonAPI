from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Getting user cases")
class TestUserGet(BaseCase):
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Unauthorised user gets only username by user ID")
    @allure.description("This test returns only username if user details are requested by unauthorised user")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User gets all user data by their user ID")
    @allure.description("This test returns all user details when user requests details about themselves")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step("Log in"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Get user details"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
                )

        with allure.step("Check that the following fields got received: {expected_fields}"):
            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User gets gets only username by ID of another user")
    @allure.description("This test returns only username if user requests details about another user")
    def test_get_user_details_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Log in"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Get details of another user"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method-1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Check that only username got received"):
            expected_field = "username"
            expected_absent_fields = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_key(response2, expected_field)
            Assertions.assert_json_has_not_keys(response2, expected_absent_fields)
