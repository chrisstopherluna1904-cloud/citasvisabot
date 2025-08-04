import os
import json
import time
import requests
from telegram import Bot

print("🚀 Iniciando bot...")

# Leer variable de entorno
cookie_str = os.environ.get("COOKIE_JSON")
if not cookie_str:
    print("❌ COOKIE_JSON no está definida en variables de entorno.")
    exit(1)

print("✅ COOKIE_JSON detectada. Cargando...")

try:
    cookies = json.loads(cookie_str)
    print("✅ Cookies cargadas correctamente.")
except json.JSONDecodeError as e:
    print(f"❌ Error al decodificar COOKIE_JSON: {e}")
    exit(1)

# Tus datos de Telegram
BOT_TOKEN = "6622686812:AAH-BsmtehRjZKiVkoKwDkgqladmeXZikn4"
USER_ID = "5895801825"

bot = Bot(token=BOT_TOKEN)

def revisar_citas():
    print("🔍 Revisando citas disponibles...")

    try:
        url = "https://ais.usvisa-info.com/es-mx/niv/schedule/13639767/appointment/days/119.json?appointments[expedite]=false"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code != 200:
            print(f"⚠️ Error en la solicitud: {response.status_code}")
            return

        data = response.json()
        if data:
            fecha = data[0]["date"]
            print(f"📆 Cita disponible: {fecha}")
            mensaje = f"✅ ¡Cita más cercana disponible!: {fecha}"
            bot.send_message(chat_id=USER_ID, text=mensaje)
        else:
            print("❌ No hay citas disponibles.")
    except Exception as e:
        print(f"❌ Error revisando citas: {e}")

while True:
    revisar_citas()
    time.sleep(60)
