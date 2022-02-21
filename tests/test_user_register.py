from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import allure


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    absent_mandatory_fields = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Create user")
    @allure.description("This test creates a user")
    def test_create_user_successfully(self):
        with allure.step("Create user"):
            data = self.prepare_registration_data()

            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that ID of newly created user got received in response"):
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User cannot be created with already existing email")
    @allure.description("This test tries to create a user with already existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        with allure.step("Try to create user with already existing email {email}"):
            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that HTTP status code 400 got received with error message"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, f"Users with email '{email}' already exists")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User cannot be created with email in invalid format")
    @allure.description("This test tries to create a user with email without @ character")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        with allure.step("Try to create user with invalid email {email}"):
            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that HTTP status code 400 got received with error message"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "Invalid email format")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User cannot be created without {absent_mandatory_field}")
    @allure.description("This test tries to create a user without one of mandatory fields")
    @pytest.mark.parametrize("absent_mandatory_field", absent_mandatory_fields)
    def test_create_user_without_mandatory_field(self, absent_mandatory_field):
        data = self.prepare_registration_data()
        data.pop(absent_mandatory_field)

        with allure.step("Try to create user without {absent_mandatory_field}"):
            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that HTTP status code 400 got received with error message"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, f"The following required params are missed: {absent_mandatory_field}")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User cannot be created with short username")
    @allure.description("This test tires to create a user with one character long username")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data["username"] = "A"

        with allure.step("Try to create user with short username"):
            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that HTTP status code 400 got received with error message"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "The value of 'username' field is too short")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User cannot be created with long username")
    @allure.description("This test tries to create a user with 251 chars long name")
    def test_create_user_with_long_username(self):
        username_length = 251
        data = self.prepare_registration_data()
        data["username"] = "A" * username_length

        with allure.step("Try to create user with long username"):
            response = MyRequests.post(
                "/user/",
                data=data
            )

        with allure.step("Check that HTTP status code 400 got received with error message"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "The value of 'username' field is too long")

