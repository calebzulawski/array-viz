import json
import requests

url = 'http://localhost:5000'
headers = {'content-type': 'application/json'}

for _ in range(5):
    new_array = {'name': u'Test', 'data': [0.1, 1.2, 3.8, 5.5]}
    data = json.dumps(new_array)
    r = requests.post(url + '/api/array', data=data, headers=headers)
    print(r.status_code, r.content)

r = requests.get(url + '/api/arrays')
print(r.status_code, r.content)

r = requests.delete(url + '/api/array', data=json.dumps({'id': 3}), headers=headers)
print(r.status_code, r.content)

r = requests.get(url + '/api/array', data=json.dumps({'id': 3}), headers=headers)
print(r.status_code, r.content)

r = requests.get(url + '/api/array', data=json.dumps({'id': 4}), headers=headers)
print(r.status_code, r.content)
