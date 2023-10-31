import requests

response = requests.post('http://127.0.0.1:8000',json={'policy_id':'reik'})

print(response.text)