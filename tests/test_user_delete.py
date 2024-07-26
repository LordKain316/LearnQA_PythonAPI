from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_user_delete(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # LOGIN
        response = MyRequests.post("/user/login/", data=data)
        print(response.text)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            f"/user/2",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400), f"Unexpected status code: '{response2.status_code}'"
        assert response2.text == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}'
        print(response2.content)

    def test_user_delete_positive(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      header={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200), f"Unexpected status code: '{response2.status_code}'"
        assert response3.text == '{"success":"!"}'

        # GET
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response4, 404), f"Unexpected status code: '{response2.status_code}'"
        assert response4.text == 'User not found'

    def test_user_delete_under_another_user(self):
        # REGISTER user 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id_1 = self.get_json_value(response1, "id")

        # REGISTER user 2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']

        # LOGIN as user 2
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response3 = MyRequests.post("/user/login/", data=login_data2)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE User 1 as User 2
        response4 = MyRequests.delete(
            f"/user/{user_id_1}",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 400), f"Unexpected status code: '{response4.status_code}'"
        a = response4.json()
        answer = a["error"]

        assert answer == 'This user can only delete their own account.', f"User was deleted"
