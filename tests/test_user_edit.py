import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import logging

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        logging.info(f"Creating new user {register_data['email']}")
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

        assert r4.status_code == 200, "Wrong status code"
        Assertions.assert_json_value_by_name(r4, 'firstName', new_name, "Wrong name of the user after edit")

    def test_edit_just_created_user_by_unauth_user(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        logging.info(f"Creating new user {register_data['email']}")
        r1 = requests.post(url_create_user, data=register_data)

        assert r1.status_code == 200, "Wrong status code"
        Assertions.assert_json_have_key(r1, "id")

        email = register_data['email']
        fist_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(r1, "id")

        new_name = "Changed"
        url_edit_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r3 = requests.put(url_edit_user, data={"firstName": new_name})

        assert r3.status_code == 400, "Wrong status code"
        assert r3.text == 'Auth token not supplied'

    def test_edit_another_user(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        logging.info(f"Creating new user {register_data['email']}")
        r1 = requests.post(url_create_user, data=register_data)

        assert r1.status_code == 200, "Wrong status code"
        Assertions.assert_json_have_key(r1, "id")

        email = register_data['email']
        fist_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(r1, "id")

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
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

        assert r3.status_code == 400, "Wrong status code"

    def test_edit_user_mail(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        logging.info(f"Creating new user {register_data['email']}")
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

        new_mail = email.replace('@', '')
        url_edit_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r3 = requests.put(url_edit_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                          data={"email": new_mail})

        assert r3.status_code == 400, "Wrong status code"
        assert r3.text == 'Invalid email format', "Wrong message"

    def test_edite_user_wrong_name(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        logging.info(f"Creating new user {register_data['email']}")
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

        new_name = "V"
        url_edit_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r3 = requests.put(url_edit_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                          data={"firstName": new_name})

        assert r3.status_code == 400, "Wrong status code"
        assert r3.json()['error'] == 'Too short value for field firstName'