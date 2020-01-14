import requests

# r = requests.get('http://neu-style.appspot.com/form')

# r = requests.post('http://neu-style.appspot.com/submitted', data{})
# r = requests.post('http://34.82.174.216:5000/Made2Morph', data={'input': 'why are you Romeo'})
r = requests.post('http://34.82.174.216:5000/Made2Morph', data={'input': 'why are you Romeo'})

print(r.text)

