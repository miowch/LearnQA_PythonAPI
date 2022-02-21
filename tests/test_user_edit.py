from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Editing user cases")
class TestUserEdit(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User changes their first name")
    @allure.description("This test changes a name of newly created user")
    def test_edit_just_created_user(self):
        with allure.step("Create user"):
            register_data = self.prepare_registration_data()
            user_id = self.register_user(register_data)

        with allure.step("Log in as newly created user"):
            login_data = {
                'email': register_data["email"],
                'password': register_data["password"],
            }

            auth_sid, token = self.log_in(login_data)

        with allure.step("Change first name to {new_name}"):
            new_name = "Changed Name"
            response_edit = self._edit_user(user_id, token, auth_sid, "firstName", new_name)
            Assertions.assert_code_status(response_edit, 200)

        with allure.step("Check that new name gets returned in user details"):
            response_get = self.get_user(user_id, token, auth_sid)

            Assertions.assert_json_value_by_name(
                response_get,
                "firstName",
                new_name,
                "Wrong username after edit"
            )

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Unauthorised user cannot change user data")
    @allure.description("This test tries to change a name of user without authentication data")
    def test_edit_user_not_auth(self):
        new_name = "Changed Name"

        with allure.step("Change first name being not authorised"):
            response = MyRequests.put(
                f"/user/2",
                data={"firstName": new_name}
            )

        with allure.step("Check that authorisation is required for editing user details"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "Auth token not supplied")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("User changes their data even though another user ID was provided")
    @allure.description("This test changes a name of authorised user when their id differs from one to be edited")
    def test_edit_user_as_another_user(self):
        new_name = "Changed Name"

        with allure.step("Create user A that should be changed"):
            register_data_user_to_be_changed = self.prepare_registration_data()
            id_of_user_to_be_changed = self.register_user(register_data_user_to_be_changed)

        with allure.step("Create user B that will change user details"):
            register_data_another_user = self.prepare_registration_data()
            id_of_another_user = self.register_user(register_data_another_user)

        with allure.step("Log in as user B"):
            login_data_another_user = {
                'email': register_data_another_user["email"],
                'password': register_data_another_user["password"],
            }

            auth_sid_of_another_user, token_of_another_user = self.log_in(login_data_another_user)

        with allure.step("Send request to change first name of user A to {new_name}"):
            response_edit = self._edit_user(
                id_of_user_to_be_changed,
                token_of_another_user,
                auth_sid_of_another_user,
                "firstName",
                new_name
            )
            Assertions.assert_code_status(response_edit, 200)

        with allure.step("Check that first name of logged in user B got changed instead"):
            response_get_another_user = self.get_user(
                id_of_another_user,
                token_of_another_user,
                auth_sid_of_another_user
            )

            Assertions.assert_json_value_by_name(
                response_get_another_user,
                "firstName",
                new_name,
                "Wrong username after edit"
            )

        with allure.step("Log in as user A"):
            login_data_user_to_be_changed = {
                'email': register_data_user_to_be_changed["email"],
                'password': register_data_user_to_be_changed["password"],
            }

            auth_sid_of_user_to_be_changed, token_of_user_to_be_changed = self.log_in(login_data_user_to_be_changed)

        with allure.step("Check that first name of user A wasn't changed"):
            response_get_user_to_be_changed = self.get_user(
                id_of_user_to_be_changed,
                token_of_user_to_be_changed,
                auth_sid_of_user_to_be_changed)

            Assertions.assert_json_value_by_name(
                response_get_user_to_be_changed,
                "firstName",
                register_data_user_to_be_changed["firstName"],
                "First name was changed by another user!"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("User cannot change email to one in invalid format")
    @allure.description("This test tries to change email to one without @ character")
    def test_change_email_to_incorrect(self):
        with allure.step("Create user"):
            register_data = self.prepare_registration_data()
            user_id = self.register_user(register_data)

        with allure.step("Log in as newly created user"):
            login_data = {
                'email': register_data["email"],
                'password': register_data["password"],
            }

            auth_sid, token = self.log_in(login_data)

        with allure.step("Change email to one in invalid format"):
            new_email = 'vinkotovexample.com'
            response = self._edit_user(user_id, token, auth_sid, "email", new_email)

        with allure.step("Check that email cannot be changed to one in invalid format"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, "Invalid email format")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User cannot change username to short one")
    @allure.description("This test tries to change username to one with one character length")
    def test_change_username_to_short(self):
        with allure.step("Create user"):
            register_data = self.prepare_registration_data()
            user_id = self.register_user(register_data)

        with allure.step("Log in as newly created user"):
            login_data = {
                'email': register_data["email"],
                'password': register_data["password"],
            }

            auth_sid, token = self.log_in(login_data)

        with allure.step("Change username to short one"):
            new_username = 'B'
            response = self._edit_user(user_id, token, auth_sid, "username", new_username)

        with allure.step("Check that username cannot be changed to one char long one"):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_error_message(response, '{"error":"Too short value for field username"}')

    @staticmethod
    @allure.step("Change {field_to_change} to {new_value}")
    def _edit_user(user_id, token, auth_sid, field_to_change, new_value):
        return MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={field_to_change: new_value}
        )
