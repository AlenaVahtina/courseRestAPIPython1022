import json

json_text = "{\"messages\":[{\"message\":\"This is the first message\",\"timestamp\":\"2021-06-04 16:40:53\"},\
{\"message\":\"And this is a second message\",\"timestamp\":\"2021-06-04 16:41:01\"}]}"
key1 = "messages"
key2 = "message"
if key1 in json.loads(json_text):
    if key2 in json.loads(json_text)[key1][1]:
        print(json.loads(json_text)[key1][1][key2])
    else:
        print(f"No key {key2} in example json")
else:
    print(f"No key {key1} in example json")