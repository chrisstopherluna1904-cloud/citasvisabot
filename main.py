import os
import json
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Cargar cookies desde variable de entorno segura
cookie_str = os.environ.get("COOKIE_JSON")
if not cookie_str:
    raise ValueError("Falta la variable COOKIE_JSON")
cookies = json.loads(cookie_str)

# Tus datos de Telegram
TELEGRAM_TOKEN = "6994692951:AAEIzW2Q9Wx5AmZD6uyAdwDJ98wDFeJVxz0"
TELEGRAM_CHAT_ID = "6667646965"
bot = Bot(token=TELEGRAM_TOKEN)

# URL con tu user_id real
URL = "https://ais.usvisa-info.com/es-mx/niv/schedule/15202751/appointment"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "es-ES,es;q=0.9"
}

ultima_fecha_enviada = ""

def revisar_disponibilidad():
    global ultima_fecha_enviada

    print("Revisando disponibilidad de citas...")
    try:
        response = requests.get(URL, headers=HEADERS, cookies=cookies)
        response.raise_for_status()
    except Exception as e:
        print("Error en la petición:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar el texto con la fecha más cercana
    fecha = None
    try:
        # Esto puede necesitar ajustes dependiendo del HTML actual
        h3 = soup.find("h3", string=lambda t: "Disponible" in t if t else False)
        if h3:
            fecha = h3.text.strip()
    except Exception as e:
        print("Error al procesar HTML:", e)

    if fecha and fecha != ultima_fecha_enviada:
        ultima_fecha_enviada = fecha
        mensaje = f"📅 ¡Nueva cita disponible!\n\n{fecha}\n\n🔗 {URL}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje)
        print("Notificación enviada.")
    else:
        print("Sin cambios en las citas.")

# Loop principal: revisa cada minuto
if __name__ == "__main__":
    while True:
        try:
            revisar_disponibilidad()
        except Exception as e:
            print("Error en el ciclo principal:", e)
        time.sleep(60)
