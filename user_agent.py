import pytest
import requests

user_agents_data = [
    {
        "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "expected": {"platform": "Mobile", "browser": "No", "device": "Android"}
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "expected": {"platform": "Mobile", "browser": "Chrome", "device": "iOS"}
    },
    {
        "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "expected": {"platform": "Googlebot", "browser": "Unknown", "device": "Unknown"}
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "expected": {"platform": "Web", "browser": "Chrome", "device": "No"}
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "expected": {"platform": "Mobile", "browser": "No", "device": "iPhone"}
    }
]


@pytest.mark.parametrize("data", user_agents_data)
def test_user_agent_check(data):
    user_agent = data["user_agent"]
    expected = data["expected"]

    header = {"User-Agent": user_agent}
    response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers=header)

    assert response.status_code == 200, "Wrong response status code"

    response_data = response.json()

    assert response_data["platform"] == expected["platform"], f"Ожидаемая платформа {expected['platform']}, но пришла {response_data['platform']}"
    assert response_data["browser"] == expected["browser"], f"Ожидаемый браузер {expected['browser']}, но пришёл {response_data['browser']}"
    assert response_data["device"] == expected["device"], f"Ожидаемое устройство {expected['device']}, но пришло {response_data['device']}"
