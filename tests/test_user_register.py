from datetime import datetime
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase, Assertions):
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

    def test_create_user_with_existing_email(self):
        self.data['email'] = 'vinkotov@example.com'

        r = requests.post(self.url_create_user, data=self.data)

        assert r.status_code == 400, f"Wrong status code {r.status_code}"
        assert r.content.decode("utf-8") == f"Users with email '{self.data['email']}' already exists", f"Wrong response {r.content}"

    def test_create_user_successfully(self):
        self.data['email'] = self.email
        r = requests.post(self.url_create_user, data=self.data)

        assert r.status_code == 200, f"Wrong status code {r.status_code}"
        Assertions.assert_json_have_key(r, "id"), "No key 'id' in response"

    def test_create_user_with_wrong_email(self):
        self.data['email'] = self.email.replace('@', '')
        r = requests.post(self.url_create_user, data=self.data)
        assert r.status_code == 400, f"Wrong status code {r.status_code}"
        assert r.content.decode("utf-8") == f"Invalid email format"

    @pytest.mark.parametrize("param", params)
    def test_create_user_without_param(self, param):
        data = {'password': '1234', 'username': 'test', 'firstName': 'test', 'lastName': 'test', "email": 'email',
                param: None}
        r = requests.post(self.url_create_user, data=data)
        assert r.status_code == 400, f"Wrong status code {r.status_code}"
        assert r.content.decode("utf-8") == f"The following required params are missed: {param}"

    def test_create_user_short_name(self):
        self.data['username'] = 'a'
        r = requests.post(self.url_create_user, data=self.data)

        assert r.status_code == 400, f"Wrong status code {r.status_code}"
        assert r.content.decode("utf-8") == f"The value of 'username' field is too short"

    def test_create_user_short_name(self):
        self.data['username'] = 'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest' \
                                'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest' \
                                'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
        r = requests.post(self.url_create_user, data=self.data)

        assert r.status_code == 400, f"Wrong status code {r.status_code}"
        assert r.content.decode("utf-8") == f"The value of 'username' field is too long"