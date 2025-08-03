[5:19 p.m., 3/8/2025] Chrisstopher Luna: [
  {
    "domain": ".usvisa-info.com",
    "name": "_gid",
    "value": "GA1.2.313422905.1754260720",
    "path": "/",
    "secure": false,
    "httpOnly": false,
    "expirationDate": 1754348100
  },
  {
    "domain": ".usvisa-info.com",
    "name": "_ga",
    "value": "GA1.2.1513135572.1754260720",
    "path": "/",
    "secure": false,
    "httpOnly": false,
    "expirationDate": 1788821700
  },
  {
    "domain": "ais.usvisa-info.com",
    "name": "_yatri_session",
    "value": "lSAMbVzv5o2qSWNdgJTqyMZytkmng3GieAeL8DliHuqfsUAURoHu5dcWptUHDTI1MEAAKA5pUHM32OflJjrH0HFZ2L9fILYNtlVtaK236PTTzvEH4iE8%2B3Dn%2FCt68m5AnSffHaPTLXY99i0CYhxyQv3%2F2Yg6lUXOq8hwPUXkEoh3YOoXbJgi6UqC0q3Rzf7utRfUqLFJddj%2BDmLUPo8jrjp94yqoqv53WVlQjnLvx5dYK04EvP1tuhO3CYTZ0XnfWgTKipzC5CINj28tQ…
[5:24 p.m., 3/8/2025] Chrisstopher Luna: import requests
import os
import json

def cargar_cookies_desde_variable():
    cookie_str = os.environ.get("COOKIE_JSON")
    if not cookie_str:
        raise ValueError("No se encontró la variable COOKIE_JSON.")
    return json.loads(cookie_str)

def revisar_citas():
    cookies = cargar_cookies_desde_variable()

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    # Aquí va tu URL real de revisión de citas
    url = "https://ais.usvisa-info.com/es-mx/niv/schedule/{tu_cita_id}"

    response = session.get(url)
    
    if "No hay citas disponibles" in response.text:
        print("❌ No hay citas disponibles.")
    else:
        print("✅ ¡Podría haber citas disponibles!")

if _name_ == "_main_":
    revisar_citas()
