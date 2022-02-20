from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        user_id = self._register_user(register_data)

        # LOG IN
        login_data = {
            'email': register_data["email"],
            'password': register_data["password"],
        }

        auth_sid, token = self._log_in(login_data)

        # EDIT
        new_name = "Changed Name"
        response_edit = self._edit_user(user_id, token, auth_sid, "firstName", new_name)
        Assertions.assert_code_status(response_edit, 200)

        # GET
        response_get = self._get_user(user_id, token, auth_sid)

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            new_name,
            "Wrong username after edit"
        )

    def test_edit_user_not_auth(self):
        new_name = "Changed Name"

        response = MyRequests.put(
            f"/user/2",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "Auth token not supplied")

    def test_edit_user_as_another_user(self):
        new_name = "Changed Name"

        # REGISTER USER TO BE CHANGED
        register_data_user_to_be_changed = self.prepare_registration_data()
        id_of_user_to_be_changed = self._register_user(register_data_user_to_be_changed)

        # REGISTER ANOTHER USER
        register_data_another_user = self.prepare_registration_data()
        id_of_another_user = self._register_user(register_data_another_user)

        # LOG IN AS ANOTHER USER
        login_data_another_user = {
            'email': register_data_another_user["email"],
            'password': register_data_another_user["password"],
        }

        auth_sid_of_another_user, token_of_another_user = self._log_in(login_data_another_user)

        # EDIT
        response_edit = self._edit_user(
            id_of_user_to_be_changed,
            token_of_another_user,
            auth_sid_of_another_user,
            "firstName",
            new_name
        )
        Assertions.assert_code_status(response_edit, 200)

        # GET LOGGED IN USER
        response_get_another_user = self._get_user(
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

        # LOG IN AS USER SUPPOSED TO BE CHANGED
        login_data_user_to_be_changed = {
            'email': register_data_user_to_be_changed["email"],
            'password': register_data_user_to_be_changed["password"],
        }

        auth_sid_of_user_to_be_changed, token_of_user_to_be_changed = self._log_in(login_data_user_to_be_changed)

        # GET USER SUPPOSED TO BE CHANGED
        response_get_user_to_be_changed = self._get_user(
            id_of_user_to_be_changed,
            token_of_user_to_be_changed,
            auth_sid_of_user_to_be_changed)

        Assertions.assert_json_value_by_name(
            response_get_user_to_be_changed,
            "firstName",
            register_data_user_to_be_changed["firstName"],
            "First name was changed by another user!"
        )

    def test_change_email_to_incorrect(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        user_id = self._register_user(register_data)

        # LOG IN
        login_data = {
            'email': register_data["email"],
            'password': register_data["password"],
        }

        auth_sid, token = self._log_in(login_data)

        # EDIT
        new_email = 'vinkotovexample.com'
        response = self._edit_user(user_id, token, auth_sid, "email", new_email)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, "Invalid email format")

    def test_change_username_to_short(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        user_id = self._register_user(register_data)

        # LOG IN
        login_data = {
            'email': register_data["email"],
            'password': register_data["password"],
        }

        auth_sid, token = self._log_in(login_data)

        # EDIT
        new_username = 'B'
        response = self._edit_user(user_id, token, auth_sid, "username", new_username)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_error_message(response, '{"error":"Too short value for field username"}')

    def _register_user(self, register_data):
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        return user_id

    def _log_in(self, login_data):
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        return auth_sid, token

    @staticmethod
    def _edit_user(user_id, token, auth_sid, field_to_change, new_value):
        return MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={field_to_change: new_value}
        )

    @staticmethod
    def _get_user(user_id, token, auth_sid):
        return MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

