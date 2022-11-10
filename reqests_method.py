import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
list_method = ["GET", "HEAD", "POST", "PUT", "DELETE",  "OPTIONS", "PATCH"]

print("Without method: ", requests.get(url).text)
print("Wrong method: ", requests.patch(url, data={"method": "PATCH"}).text)
print("Right method: ", requests.get(url, params={"method": "GET"}).text)

for method in list_method:
    for param in list_method:
        if method.__eq__("GET"):
            print("What happened with %s method with param %s: %s" % (method, param, requests.request(method, url, params={"method": param}).text))
        else:
            print("What happened with %s method with data %s: %s"%(method,param, requests.request(method, url, data={"method": param}).text))