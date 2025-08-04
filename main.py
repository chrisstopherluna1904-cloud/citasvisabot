import os
import json
import time
import requests
import telegram
from bs4 import BeautifulSoup

# Cargar TOKEN y USER_ID directamente
TELEGRAM_BOT_TOKEN = '6678632346:AAFYoQoW-LchG3cKDbYBlRWTmLKkUZ_kkeY'
USER_ID = 1410074532

# Inicializar bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# Leer cookies desde variable de entorno
cookies_str = os.getenv("COOKIE_JSON")
if not cookies_str:
    raise Exception("COOKIE_JSON no está definida en las variables de entorno")

cookies = json.loads(cookies_str)

# URL de la página de citas (ajusta si es otra)
URL = "https://ais.usvisa-info.com/es-mx/niv/schedule/44200000/appointment"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://ais.usvisa-info.com/es-mx/niv"
}

def check_appointment():
    response = requests.get(URL, headers=headers, cookies=cookies)

    if response.status_code != 200:
        print(f"Error al consultar la página. Código {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Esto depende de cómo venga la cita en el HTML, ajústalo si es diferente:
    available = soup.find('h3')

    if available:
        text = available.get_text(strip=True)
        bot.send_message(chat_id=USER_ID, text=f"📅 Cita más cercana disponible:\n\n{text}")
        print("Mensaje enviado por Telegram")
    else:
        print("No se encontró ninguna cita disponible")

if __name__ == "__main__":
    while True:
        try:
            check_appointment()
        except Exception as e:
            print(f"Error en la ejecución: {e}")
        time.sleep(60)  # Espera 60 segundos antes de revisar otra vez
