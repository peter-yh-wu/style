import requests


r = requests.post('http://35.233.173.95:5000/elon', data={'input': 'turn this into elon sentence'})
print(r.text)


r = requests.post('http://35.233.173.95:5000/obama', data={'input': 'turn this into obama sentence'})
print(r.text)


r = requests.post('http://35.233.173.95:5000/trump', data={'input': 'turn this into trump sentence'})
print(r.text)
