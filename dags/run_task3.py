import json

import requests

LOGIN_API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjdlYjlhN2UtNjdjZS00YmZkLTliYTYtZDBkNTNjOTg3YWQzIiwiZXhwIjoxNzI5NDk3MTk2LCJpc3MiOiJTRUxGX0hPU1RFRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.xIsij0yPbvs4wUvCw8sykbqp2F5WaY5YSnBg_mdR5xA"
url = "http://159.75.168.215/console/api/apps/9d7ff4a1-eefc-4e33-88b4-f0b7572a4ce7/workflows/draft/run"

payload = json.dumps(
    {"inputs": {"link": "https://rsshub.app/eastmoney/search/web3"}, "files": []}
)
headers = {"authorization": LOGIN_API_KEY, "content-type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
