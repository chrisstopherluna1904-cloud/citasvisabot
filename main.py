import requests
import time
import json

# ==== CONFIGURACIÓN DEL USUARIO ====
TELEGRAM_BOT_TOKEN = "6750084511:AAHPQwYcYBQOv0kBoOBbcS3HLaZX9LmPK8I"
TELEGRAM_USER_ID = "687136291"
CHECK_INTERVAL_SECONDS = 60  # 1 minuto

# ==== URL de verificación (ajusta si es necesario) ====
APPOINTMENT_URL = "https://ais.usvisa-info.com/es-mx/niv/schedule/53819864/appointment"

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
if __name__ == "__main__":
    while True:
        check_appointment()
        time.sleep(CHECK_INTERVAL_SECONDS)
