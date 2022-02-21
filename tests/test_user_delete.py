import time

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Deletion user cases")
class TestUserDelete(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Delete user")
    @allure.description("This test successfully deletes user")
    def test_delete_user_successfully(self):
        with allure.step("Create user"):
            register_data = self.prepare_registration_data()
            user_id = self.register_user(register_data)

        with allure.step("Log in as newly created user"):
            login_data = {
                'email': register_data["email"],
                'password': register_data["password"],
            }

            auth_sid, token = self.log_in(login_data)

        with allure.step("Delete logged in user"):
            MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Check that no user can be found by ID of deleted user"):
            response = MyRequests.get(f"/user/{user_id}")

            Assertions.assert_code_status(response, 404)
            Assertions.assert_error_message(response, "User not found")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User created for learning purposes cannot be deleted")
    @allure.description("This test tries to delete test user that is blocked from being deleted")
    def test_delete_user_created_for_learning_purposes(self):
        with allure.step("Log in as test user with email {login_data['email']}"):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            auth_sid, token = self.log_in(login_data)

        with allure.step("Delete the user"):
            response = MyRequests.delete(
                "/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Check that test user cannot be deleted"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User cannot delete another user")
    @allure.description("This test deletes authorised user when their id differs from one to be deleted")
    def test_delete_user_as_another_user(self):
        with allure.step("Create user A that should be deleted"):
            register_data_user_to_be_deleted = self.prepare_registration_data()
            id_of_user_to_be_deleted = self.register_user(register_data_user_to_be_deleted)

        with allure.step("Create user B that will perform deletion"):
            time.sleep(2)
            register_data_another_user = self.prepare_registration_data()
            id_of_another_user = self.register_user(register_data_another_user)

        with allure.step("Log in as user B that should perform deletion"):
            login_data_another_user = {
                'email': register_data_another_user["email"],
                'password': register_data_another_user["password"],
            }

            auth_sid_of_another_user, token_of_another_user = self.log_in(login_data_another_user)

        with allure.step("Delete user A that was created on the first step"):
            response_delete = MyRequests.delete(
                f"/user/{id_of_user_to_be_deleted}",
                headers={"x-csrf-token": token_of_another_user},
                cookies={"auth_sid": auth_sid_of_another_user}
            )
        with allure.step("Check that HTTP status code 200 got returned"):
            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Check that logged in user B cannot be retrieved with error message 'User not found'"):
            response_get_another_user = MyRequests.get(f"/user/{id_of_another_user}")

            Assertions.assert_code_status(response_get_another_user, 404)
            Assertions.assert_error_message(response_get_another_user, "User not found")

        # GET USER SUPPOSED TO BE DELETED
        with allure.step("Check that user A still exists"):
            response_get_user_to_be_deleted = MyRequests.get(f"/user/{id_of_user_to_be_deleted}")

            Assertions.assert_json_has_key(response_get_user_to_be_deleted, "username")
