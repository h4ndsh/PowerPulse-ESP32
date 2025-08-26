import time
import urequests
import boot
import jwt   # ⚠️ Precisas de micropython-jwt, ou implementamos uma versão mínima

JWT_SECRET = "your_jwt_secret"
URL = 'https://your-url.com/hello'

config = boot.load_config()
NAME = config.get("name") if config else "ESP32-DEFAULT"

def make_jwt():
    payload = {"sub": NAME}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

while True:
    try:
        token = make_jwt()
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        data = {
            "name": NAME,
            "time": time.time()
        }
        r = urequests.post(URL, headers=headers, json=data)
        print("Resposta:", r.text)
        r.close()
    except Exception as e:
        print("Erro no envio:", e)

    time.sleep(300)  # 5 minutos
