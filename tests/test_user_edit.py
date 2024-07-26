from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
            )

        Assertions.assert_code_status(response3, 200)

        # get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4, "firstName", new_name,
            "Wrong name of the user after edit")

        print(response4.text)

    def test_edit_user_unauthorized(self):
        response2 = MyRequests.put(
            f"/user/101623",
            data={"firstName": "vasya"}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.text == '{"error":"Auth token not supplied"}'

    def test_edit_user_as_different_user(self):
        # Register first user
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id1 = self.get_json_value(response1, "id")  # получает ID первого пользователя

        # Register second user
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']

        # Login as the second user
        login_data = {
            'email': email2,
            'password': password2
        }
        response3 = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Try to edit first user's data
        response4 = MyRequests.put(
            f"/user/{user_id1}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "Petya"}
        )

        Assertions.assert_code_status(response4, 400)
        assert response4.text == '{"error":"This user can only edit their own data."}'

    def test_edit_user_invalid_email(self):
        # Register user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login user
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Try to change email to invalid
        response3 = MyRequests.put(
            f"/user/{user_id}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": "invalidemail.com"}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.text == '{"error":"Invalid email format"}'


    def test_edit_user_short_name(self):
        # Register a user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login user
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Attempt to change firstName to a very short value
        response3 = MyRequests.put(
            f"/user/{user_id}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "A"}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.text == '{"error":"The value for field `firstName` is too short"}'