#!/usr/bin/python3

import re
import threading
import time
import datetime
import os
import requests
import jwt
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHATS = os.getenv('TELEGRAM_CHATS').split(',')
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))
INTERVAL_SECONDS = CHECK_INTERVAL_MINUTES * 60
MISS_THRESHOLD = int(os.getenv('MISS_THRESHOLD', 5))
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
ALERT_TEMPLATE = os.getenv('ALERT_TEMPLATE', 'Casa "{name}" sem energia !\n!\nCASA: {name}\nHORA DA FALHA DE ENERGIA: {time}')

app = Flask(__name__)

clients = {}  # {name: {'last_time': datetime, 'miss_count': int, 'alerted': bool}}
lock = threading.Lock()


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)
    return True

def check_clients():
    while True:
        time.sleep(INTERVAL_SECONDS)
        with lock:
            now = datetime.datetime.now()
            for name, data in list(clients.items()):
                if (now - data['last_time']).total_seconds() > INTERVAL_SECONDS:
                    data['miss_count'] += 1
                    if data['miss_count'] >= MISS_THRESHOLD and not data.get('alerted', False):
                        time_str = clients[name]['last_time'].strftime("%H:%M %d-%m-%Y")
                        message = (
                            f"⚠️ <b>ALERTA DE ENERGIA</b>\n\n"
                            f"🏠 Casa <b>{name.upper()}</b>\n"
                            f"⏰ Hora da Falha: <b>{time_str}</b>"
                        )
                        for chat in TELEGRAM_CHATS:
                            send_telegram_message(chat, message)
                        data['alerted'] = True

@app.route('/hello', methods=['POST'])
def hello():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return 'Unauthorized', 401
    token = auth.split()[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        name_from_token = payload['sub']
    except:
        return 'Unauthorized', 401

    json_data = request.get_json()
    if not json_data or 'name' not in json_data or 'time' not in json_data:
        return 'Bad request', 400
    if json_data['name'] != name_from_token:
        return 'Mismatch', 403

    name = json_data['name']

    with lock:
        now = datetime.datetime.now()
        if name not in clients:
            clients[name] = {'last_time': now, 'miss_count': 0, 'alerted': False}
        else:
            clients[name]['last_time'] = now
            clients[name]['miss_count'] = 0
            clients[name]['alerted'] = False

    return 'OK', 200

if __name__ == '__main__':
    checker_thread = threading.Thread(target=check_clients)
    checker_thread.daemon = True
    checker_thread.start()
    app.run(host=SERVER_HOST, port=SERVER_PORT)