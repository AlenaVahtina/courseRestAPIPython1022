import requests

class TestExample:

    def test_cookie(self):
        url_homework_cookie = 'https://playground.learnqa.ru/api/homework_cookie'
        session = requests.Session()
        r = session.get(url_homework_cookie)
        cookie = session.cookies.get_dict()
        assert "HomeWork" in cookie.keys(), f"Expected 'HomeWork' key in cookie dict {cookie.keys()}"
        assert cookie["HomeWork"] == "hw_value", f"Value of cookie 'HomeWork' is {cookie['HomeWork']} but 'hw_value' expected"