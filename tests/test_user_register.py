from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserRegister(BaseCase):
    absent_mandatory_fields = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, f"Users with email '{email}' already exists")

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "Invalid email format")

    @pytest.mark.parametrize("absent_mandatory_field", absent_mandatory_fields)
    def test_create_user_without_mandatory_field(self, absent_mandatory_field):
        data = self.prepare_registration_data()
        data.pop(absent_mandatory_field)

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, f"The following required params are missed: {absent_mandatory_field}")

    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data["username"] = "A"

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "The value of 'username' field is too short")

    def test_create_user_with_long_username(self):
        username_length = 251
        data = self.prepare_registration_data()
        data["username"] = "A" * username_length

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "The value of 'username' field is too long")

