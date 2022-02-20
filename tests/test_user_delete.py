from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserDelete(BaseCase):
    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        user_id = self.register_user(register_data)

        # LOG IN
        login_data = {
            'email': register_data["email"],
            'password': register_data["password"],
        }

        auth_sid, token = self.log_in(login_data)

        # DELETE
        MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # GET
        response = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_code_status(response, 404)
        Assertions.assert_error_message(response, "User not found")

    def test_delete_user_created_for_learning_purposes(self):
        # LOG IN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        auth_sid, token = self.log_in(login_data)

        # DELETE
        response = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    def test_delete_user_as_another_user(self):
        # REGISTER USER TO BE DELETED
        register_data_user_to_be_deleted = self.prepare_registration_data()
        id_of_user_to_be_deleted = self.register_user(register_data_user_to_be_deleted)

        # REGISTER ANOTHER USER
        register_data_another_user = self.prepare_registration_data()
        id_of_another_user = self.register_user(register_data_another_user)

        # LOG IN AS ANOTHER USER
        login_data_another_user = {
            'email': register_data_another_user["email"],
            'password': register_data_another_user["password"],
        }

        auth_sid_of_another_user, token_of_another_user = self.log_in(login_data_another_user)

        # DELETE
        response_delete = MyRequests.delete(
            f"/user/{id_of_user_to_be_deleted}",
            headers={"x-csrf-token": token_of_another_user},
            cookies={"auth_sid": auth_sid_of_another_user}
        )
        Assertions.assert_code_status(response_delete, 200)

        # GET LOGGED IN USER
        response_get_another_user = MyRequests.get(f"/user/{id_of_another_user}")

        Assertions.assert_code_status(response_get_another_user, 404)
        Assertions.assert_error_message(response_get_another_user, "User not found")

        # GET USER SUPPOSED TO BE DELETED
        response_get_user_to_be_deleted = MyRequests.get(f"/user/{id_of_user_to_be_deleted}")

        Assertions.assert_json_has_key(response_get_user_to_be_deleted, "username")
