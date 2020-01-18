import requests

# r = requests.get('http://neu-style.appspot.com/form')

# r = requests.post('http://neu-style.appspot.com/submitted', data{})
# r = requests.post('http://34.82.174.216:5000/Made2Morph', data={'input': 'why are you Romeo'})
# r = requests.post('http://34.82.174.216:5000/Made2Morph', data={'input': 'why are you Romeo'})

# r = requests.post('http://34.82.174.216:5000/neg', data={'input': 'this is great'})

r = requests.post('http://34.83.30.177:5000/elon', data={'input': 'turn this into elon sentence'})
print(r.text)


r = requests.post('http://34.82.174.216:5000/obama', data={'input': 'turn this into obama sentence'})
print(r.text)


r = requests.post('http://104.196.253.238:5000/trump', data={'input': 'turn this into trump sentence'})
print(r.text)
