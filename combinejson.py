import pandas as pd
import glob, os, json
from pprint import pprint


def find_between(s, first, last):
    try:
        if (s.find(first) != -1):
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        else:
            return s
    except ValueError:
        return "message not found"


def is_existing_key(data):
    try:
        msg = 'message not found'
        for dt in data:
            if "msg" in dt:
                return dt["msg"]
        return msg
    except ValueError:
        return "type error"

json_dir = 'data/json_files_dir'

json_pattern = os.path.join(json_dir, '*.json')
file_list = glob.glob(json_pattern)
dfs = []
for file in file_list:
    with open(file, 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
        if json_data["type"] == 'chat':
            msg = is_existing_key(json_data['messages'])
            newPerson = {
                "type": json_data['type'],
                "email": json_data['visitor']['email'],
                "name": json_data['visitor']['name'],
                "message": find_between(msg, 'Apa yang bisa kami bantu ? :\r\n ', '\r\n\r\nName :'),
                "createdOn": json_data['createdOn'],
            }
        else:

            newPerson = {
                "type": json_data['type'],
                "email": json_data['requester']['email'],
                "name": json_data['requester']['name'],
                "message": json_data['events'][0]['data']['message'] if len(json_data['events']) > 0 else '',
                "createdOn": json_data['createdOn'],
            }
    dfs.append(newPerson)
json_object = json.dumps(dfs, indent=5)
with open("result.json", "w") as outfile:
    outfile.write(json_object)
