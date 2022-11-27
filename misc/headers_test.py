import requests


class TestExample:

    def test_cookie(self):
        url_homework_header = 'https://playground.learnqa.ru/api/homework_header'
        r = requests.get(url_homework_header)
        assert "Some secret value" == r.headers['x-secret-homework-header'], f"Value of header x-secret-homework-header" \
                                                                             f" is {r.headers['x-secret-homework-header']}"