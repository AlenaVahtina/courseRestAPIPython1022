from datetime import datetime
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Test delete user")
class TestUserDelete(BaseCase, Assertions):

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

    @allure.description("Delete user vinkotov@example.com")
    def test_delete_default_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        allure.step("Step 1: login user vinkotov")

        url_login = "https://playground.learnqa.ru/api/user/login"
        r1 = requests.post(url_login, data=data)

        assert r1.status_code == 200, "Wrong status code"

        auth_sid = self.get_cookie(r1, "auth_sid")
        token = self.get_header(r1, "x-csrf-token")
        user_id = self.get_json_value(r1, "user_id")

        allure.step("Step 2: auth user vinkotov")
        url_auth = 'https://playground.learnqa.ru/api/user/auth'
        r2 = requests.get(url_auth, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r2.status_code == 200, "Wrong status code"

        allure.step("Step 3: delete user vinkotov")
        url_delete_user = f"https://playground.learnqa.ru/api/user/{user_id}"
        r3 = requests.delete(url_delete_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r3.status_code == 400, "Wrong status code"
        assert r3.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", "Wrong text message"

    @allure.description("Delete just created user")
    def test_delete_user(self):
        allure.step("Step 1: create user")
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

        allure.step(f"Step 2: login user {email}")
        url_login = "https://playground.learnqa.ru/api/user/login"
        r2 = requests.post(url_login, data=login_data)

        assert r2.status_code == 200, "Wrong status code"

        auth_sid = self.get_cookie(r2, "auth_sid")
        token = self.get_header(r2, "x-csrf-token")

        allure.step(f"Step 3: delete user {email}")
        url_delete_user = f"https://playground.learnqa.ru/api/user/{user_id}"
        r3 = requests.delete(url_delete_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r3.status_code == 200, "Wrong status code"

        allure.step(f"Step 4: check user {email}")
        url_check_user = f'https://playground.learnqa.ru/api/user/{user_id}'
        r4 = requests.get(url_check_user, headers={"x-csrf-token": None}, cookies={"auth_sid": None})

        assert r4.status_code == 404, "Wrong status code"
        assert r4.text == "User not found", f"User {email} has not been deleted"

    def test_delete_other_user(self):
        url_create_user = 'https://playground.learnqa.ru/api/user/'
        register_data = self.prepare_registration_data()
        r1 = requests.post(url_create_user, data=register_data)

        assert r1.status_code == 200, "Wrong status code"
        Assertions.assert_json_have_key(r1, "id")

        user_id_to_del = self.get_json_value(r1, "id")

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        url_login = "https://playground.learnqa.ru/api/user/login"
        r2 = requests.post(url_login, data=login_data)

        assert r2.status_code == 200, "Wrong status code"

        auth_sid = self.get_cookie(r2, "auth_sid")
        token = self.get_header(r2, "x-csrf-token")

        url_auth = 'https://playground.learnqa.ru/api/user/auth'
        r3 = requests.get(url_auth, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r3.status_code == 200, "Wrong status code"

        url_delete_user = f"https://playground.learnqa.ru/api/user/{user_id_to_del}"
        r4 = requests.delete(url_delete_user, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        assert r4.status_code == 400, "Wrong status code"
