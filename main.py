import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# DATOS REALES
TELEGRAM_TOKEN = "6775977127:AAGWEpI9y9ZLZ9RHutvtrQvATzRivm9Xbqs"
TELEGRAM_CHAT_ID = "542595976"
URL_CITAS = "https://ais.usvisa-info.com/es-mx/niv/schedule/48812804/appointment"
COOKIES = {
    "_yatri_session": "1pEyUKE+MvhLB2NSBL+ymqQci8SxgdV5DEBiUaaHTm9D0dnZxd5a2m8R52RQJSjPWViSKtS3q2zJq58T4OY9RxFGBTL1QZcHNOv8d5YXTVg="
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Buscar citas antes de esta fecha (año, mes, día)
UMBRAL_FECHA = (2026, 6, 1)  # ejemplo: cualquier cita antes de junio 2026

def obtener_fecha():
    try:
        response = requests.get(URL_CITAS, cookies=COOKIES, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        tag = soup.find("h3")
        if not tag:
            return None

        fecha_str = tag.get_text(strip=True)
        print(f"[INFO] Fecha encontrada: {fecha_str}")

        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
            'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
            'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        partes = fecha_str.lower().split()
        if len(partes) != 3:
            return None

        dia = int(partes[0])
        mes = meses.get(partes[1], 0)
        año = int(partes[2])
        return (año, mes, dia)

    except Exception as e:
        print(f"[ERROR] Al obtener fecha: {e}")
        return None

def enviar_telegram(mensaje):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje)
        print("[INFO] Notificación enviada")
    except Exception as e:
        print(f"[ERROR] Al enviar Telegram: {e}")

def es_menor(fecha):
    return fecha < UMBRAL_FECHA

# Bucle principal
while True:
    fecha = obtener_fecha()

    if fecha and es_menor(fecha):
        mensaje = f"¡Nueva cita disponible! 📅 {fecha[2]}/{fecha[1]}/{fecha[0]}\n{URL_CITAS}"
        enviar_telegram(mensaje)

    time.sleep(60)  # Espera 60 segundos
