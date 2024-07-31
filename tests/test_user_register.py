from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Tests for users")
@allure.feature("Register cases")
class TestUserRegister(BaseCase):
    email = 'vinkotov@example.com'

    @allure.description("This test successfully create new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test correctly checks for invalid email when registering a user")
    def test_uncorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"Expected server response: '{response.text}'"

    @pytest.mark.parametrize("missing_field", ["password", "username", "firstName", "lastName", "email"])
    @allure.description("This test successfully checks registration with not full params")
    def test_create_user_missing_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {missing_field}", \
            f"Unexpected response content: {response.text}"

    @allure.description("This test checks successfully that you can't registration this too short username")
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

    @allure.description("This test successfully checks that you can't registration this too long username")
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

    @allure.description("This test checks that you can't register with existing email")
    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data(self.email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{self.email}' already exists", f"Unexpected response content {response.content}"
