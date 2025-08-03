import requests
import time
import json

# ==== CONFIGURACIÓN DEL USUARIO ====
TELEGRAM_BOT_TOKEN = "TU_TOKEN_DE_BOT"
TELEGRAM_USER_ID = "TU_USER_ID"
CHECK_INTERVAL_SECONDS = 60  # 1 minuto

# ==== URL de verificación (reemplaza por la tuya exacta si cambia) ====
APPOINTMENT_URL = "https://ais.usvisa-info.com/es-mx/niv/schedule/xxxxx/appointment"

# ==== Cargar cookies ====
def load_cookies():
    with open("cookie.json", "r") as f:
        cookies = json.load(f)
    return {cookie['name']: cookie['value'] for cookie in cookies}

# ==== Función para mandar mensaje por Telegram ====
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_USER_ID, "text": message}
    requests.post(url, data=data)

# ==== Función principal ====
def check_appointment():
    cookies = load_cookies()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": APPOINTMENT_URL
    }

    try:
        response = requests.get(APPOINTMENT_URL, headers=headers, cookies=cookies)
        if "Ya tienes una cita programada" not in response.text:
            send_telegram_message("🔔 ¡Parece que hay una cita disponible!")
        else:
            print("Sin cambios en la cita.")
    except Exception as e:
        print("Error al consultar:", e)

# ==== Loop continuo ====
if _name_ == "_main_":
    while True:
        check_appointment()
        time.sleep(CHECK_INTERVAL_SECONDS)
