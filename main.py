import os
import json
import requests
import time
from telegram import Bot

# === CONFIGURACIÓN ===
TELEGRAM_BOT_TOKEN = '6733370659:AAGYJqA7UxqD6K2-rXygTSXfpFeR7dN9jS8'
TELEGRAM_USER_ID = '5421325452'

# Cargar la cookie desde la variable de entorno
cookie_str = os.environ.get("COOKIE_JSON", "")
if not cookie_str:
    raise ValueError("La variable de entorno COOKIE_JSON está vacía o no fue configurada")

try:
    cookie_dict = json.loads(cookie_str)
except json.JSONDecodeError:
    raise ValueError("COOKIE_JSON no es un JSON válido")

session = requests.Session()
session.cookies.update(cookie_dict)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# === FUNCIÓN PRINCIPAL ===
def verificar_cita():
    url = "https://ais.usvisa-info.com/es-mx/niv/schedule/54711790/appointment/days/115.html?appointments[expedite]=false"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            fechas = response.json()
            if fechas:
                fecha_mas_cercana = fechas[0]["date"]
                mensaje = f"📅 ¡Cita disponible!\nFecha más cercana: {fecha_mas_cercana}"
                bot.send_message(chat_id=TELEGRAM_USER_ID, text=mensaje)
            else:
                print("Sin fechas disponibles por ahora.")
        else:
            print(f"Error al consultar: {response.status_code}")
    except Exception as e:
        print(f"Error al verificar cita: {e}")

# === LOOP INFINITO (verifica cada minuto) ===
if __name__ == "__main__":
    while True:
        verificar_cita()
        time.sleep(60)  # Esperar 1 minuto entre cada chequeo
