import network
import ujson
import machine
import os
import socket
import time

CONFIG_FILE = "wifi.json"

def save_config(ssid, password, name):
    with open(CONFIG_FILE, "w") as f:
        f.write(ujson.dumps({
            "ssid": ssid,
            "password": password,
            "name": name
        }))

def load_config():
    if CONFIG_FILE in os.listdir():
        with open(CONFIG_FILE) as f:
            return ujson.loads(f.read())
    return None

def connect_wifi():
    config = load_config()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if config:
        print("A ligar a Wi-Fi:", config["ssid"])
        sta.connect(config["ssid"], config["password"])
        for _ in range(20):  # até ~10s
            if sta.isconnected():
                print("Ligado:", sta.ifconfig())
                return True
            time.sleep(0.5)
        print("Falha ao ligar à rede")
    return False

def start_config_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP32_Config", password="12345678")
    print("AP ativo: ESP32_Config (pass: 12345678)")

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Servidor Web pronto em http://192.168.4.1")

    while True:
        cl, addr = s.accept()
        req = cl.recv(1024).decode()
        print("Requisição:", req)

        if "POST" in req:
            try:
                body = req.split("\r\n\r\n")[1]
                params = {}
                for pair in body.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        params[k] = v.replace("%20", " ")

                ssid = params.get("ssid")
                password = params.get("password")
                name = params.get("name")
                if ssid and password and name:
                    save_config(ssid, password, name)
                    response = "<h3>Config guardada! Reinicia...</h3>"
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
                    cl.close()
                    time.sleep(2)
                    machine.reset()
            except Exception as e:
                print("Erro:", e)

        html = """<!DOCTYPE html>
                <html>
                    <head><title>Config WiFi</title></head>
                    <body>
                        <h2>Configurar Wi-Fi e Nome</h2>
                        <form method="POST">
                            SSID: <input type="text" name="ssid"><br>
                            Password: <input type="password" name="password"><br>
                            Nome (Casa): <input type="text" name="name"><br>
                            <input type="submit" value="Guardar">
                        </form>
                    </body>
                </html>
                """
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
        cl.close()

# ----- EXECUÇÃO -----
if not connect_wifi():
    start_config_ap()
