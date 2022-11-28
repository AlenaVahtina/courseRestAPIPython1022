import pytest
import requests
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        r1 = requests.post(url_create_user, data=register_data)

        assert r1.status_code == 200, "Wrong status code"
        Assertions.assert_json_have_key(r1, "id")

        email = register_data['email']
        fist_name = register_data['firstName']
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

        new_name = "Changed"
        url_edit_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r3 = requests.put(url_edit_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                          data={"firstName": new_name})

        assert r3.status_code == 200, "Wrong status code"

        url_check_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r4 = requests.get(url_check_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r3.status_code == 200, "Wrong status code"
        Assertions.assert_json_value_by_name(r4, 'firstName', new_name, "Wrong name of the user after edit")
