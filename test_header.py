import requests

class TestHeaders:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        print(response)
        assert response.status_code == 200, "Wrong response status"

        header = response.headers
        print(header)

        secret_key = header.get('x-secret-homework-header')
        print(secret_key)

        expected_key = 'Some secret value'
        assert secret_key == expected_key, "Not expected response secret-key"

        content_type = header.get('Content-Type')
        print(content_type)
        expected_type = 'application/json'
        assert content_type == expected_type, "Not expected content-type"

        connection = header.get('Connection')
        print(connection)
        expected_connection = 'keep-alive'
        assert connection == expected_connection, "Not expected connection"