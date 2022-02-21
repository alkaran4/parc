#### вариант с api
import requests
import json


url = 'https://api.github.com'
user = 'defunkt'

response = requests.get(f'{url}/users/{user}/repos')

for repo in response.json():
    print(repo['name'])

with open('repos.json', 'w') as f:
    json.dump(response.json(), f)
