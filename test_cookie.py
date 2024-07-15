import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url)

        assert response.status_code == 200, "Wrong status"

        cookie = (dict(response.cookies))

        print(cookie)
        assert "HomeWork" in cookie, "Ключ отсутствует"
        value = cookie.get('HomeWork')
        print(value)

        actual_value = value

        expected_value = 'hw_value'
        assert actual_value == expected_value, "Значение ключа не совпадает с ожидаемым"