import requests

url = "https://playground.learnqa.ru/api/long_redirect"
r = requests.get(url)
print("Number of redirects: ", len(r.history))
print("Final url: ", r.url)