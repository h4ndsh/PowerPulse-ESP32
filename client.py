import datetime
import requests
import jwt

JWT_SECRET = "your_jwt_secret"
# URL = 'https://your-url.com/hello'
NAME = "HOME"

token = jwt.encode({'sub': NAME}, JWT_SECRET, algorithm='HS256')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

data = {
    'name': NAME,
    'time': datetime.datetime.now().isoformat()
}

response = requests.post(URL, headers=headers, json=data)
print(response.text)