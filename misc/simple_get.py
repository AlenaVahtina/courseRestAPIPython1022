import requests

url = "https://playground.learnqa.ru/api/get_text"
r = requests.get(url)
print(r.text)