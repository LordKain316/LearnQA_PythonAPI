from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    email = 'vinkotov@example.com'

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_uncorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"Expected server response: '{response.text}'"

    @pytest.mark.parametrize("missing_field", ["password", "username", "firstName", "lastName", "email"])
    def test_create_user_missing_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {missing_field}", \
            f"Unexpected response content: {response.text}"

    def test_create_user_with_short_username(self):
        data = {
            'password': '123',
            'username': 'a',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short", f"Unexpected response content: {response.text}"

    def test_create_user_with_long_username(self):
        long_username = 'a' * 251
        data = {
            'password': '123',
            'username': long_username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long", f"Unexpected response content: {response.text}"

    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data(self.email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{self.email}' already exists", f"Unexpected response content {response.content}"
