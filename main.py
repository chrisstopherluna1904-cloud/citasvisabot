import requests
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

if __name__ == "__main__":
    revisar_citas()
