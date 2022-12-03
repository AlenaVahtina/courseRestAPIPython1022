from datetime import datetime
import pytest
import requests
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserReadingDataAcquisition(BaseCase, Assertions):
    params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]
    url_create_user = 'https://playground.learnqa.ru/api/user/'
    email = None
    data = {
        'password': '1234',
        'username': 'test',
        'firstName': 'test',
        'lastName': 'test',
        "email": email
    }

    def setup(self):
        base_part = 'test'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    @pytest.mark.parametrize("param", params)
    def test_get_user_data_by_unauth_user(self, param):
        user_id = 2
        url_check_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r = requests.get(url_check_user, headers={"x-csrf-token": None}, cookies={"auth_sid": None})

        assert r.status_code == 200, "Wrong status code"
        if param in r.json():
            Assertions.assert_json_value_by_name(r, param, 'Vitaliy', f"Wrong result get user param {param}")
        else:
            print(f"Right result get user param {param}")

    @pytest.mark.parametrize("param", params)
    def test_get_user_data_by_another_user(self, param):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        r1 = requests.post(url_create_user, data=register_data)

        assert r1.status_code == 200, "Wrong status code"
        Assertions.assert_json_have_key(r1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(r1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        url_login = "https://playground.learnqa.ru/api/user/login"
        r2 = requests.post(url_login, data=login_data)

        assert r2.status_code == 200, "Wrong status code"

        auth_sid = self.get_cookie(r2, "auth_sid")
        token = self.get_header(r2, "x-csrf-token")

        user_id = 2
        url_check_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r3 = requests.get(url_check_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r3.status_code == 200, "Wrong status code"
        if param in r3.json():
            Assertions.assert_json_value_by_name(r3, param, 'Vitaliy', f"Wrong result get user param {param}")
        else:
            print(f"Right result get user param {param}")

