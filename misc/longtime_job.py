import requests
import time
import json

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
token = None
step_one = requests.get(url)
live_time = json.loads(step_one.text)["seconds"]
if "token" in step_one.text:
    token = json.loads(step_one.text)["token"]

if token:
    step_two = requests.get(url, params={"token": token})
    print(json.loads(step_two.text)["status"])
else:
    print("You have not token")

print("Time to sleep", live_time)
time.sleep(live_time+1)

if token:
    step_three = requests.get(url, params={"token": token})
    if "status" in step_three.text:
        print(json.loads(step_three.text)["status"])
        if "result" in step_three.text:
            print(json.loads(step_three.text)["result"])
        else:
            print("You have not result")
    else:
        print("You have not status")