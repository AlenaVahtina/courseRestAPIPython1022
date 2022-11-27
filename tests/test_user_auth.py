import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase, Assertions):

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        url_login = "https://playground.learnqa.ru/api/user/login"
        r1 = requests.post(url_login, data=data)

        assert r1.status_code == 200, "Wrong status code"

        self.auth_sid = self.get_cookie(r1, "auth_sid")
        self.token = self.get_header(r1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(r1, "user_id")

    def test_auth_user(self):
        url_auth = 'https://playground.learnqa.ru/api/user/auth'
        r2 = requests.get(url_auth, headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})

        assert r2.status_code == 200, "Wrong status code"

        Assertions.assert_json_value_by_name(
            r2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )
