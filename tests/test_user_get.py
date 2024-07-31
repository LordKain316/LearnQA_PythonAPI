from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Tests for users")
@allure.feature("Get cases")
class TestUserGet(BaseCase):
    def setup_method(self):
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

    @allure.description("This test ckecks that you can get only name being unauthorized")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test checks that you can get all details of user being authorized him")
    def test_get_user_details_auth_as_same_user(self):

        response1 = MyRequests.post("/user/login/", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2= MyRequests.get(f"/user/{user_id_from_auth_method}",
                                header={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks that you can't get users details being login another user")
    def test_get_user_details_auth_as_different_user(self):
        response1 = MyRequests.post("/user/login/", data=self.data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        response2 = MyRequests.get(f"/user/101623",
            header={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 200), f"Unexpected status code: '{response2.status_code}'"

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
