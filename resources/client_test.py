import requests


url = 'http://127.0.0.1:8000/users/me'
_method = 'GET'
headers = ''


responce = requests.request(url=url, method=_method, params={'user_name': 'wizardx1'})

print(responce.text)