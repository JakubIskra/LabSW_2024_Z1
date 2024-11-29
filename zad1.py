from flask import Flask, request, jsonify
import logging
from datetime import datetime
import pytz
import requests

# Konfiguracja serwera
AUTHOR_NAME = "Jakub Iskra"
TCP_PORT = 5000
LOG_FILE = "server.log"

# Inicjalizacja logowania
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


# Funkcja do logowania informacji o uruchomieniu serwera
def log_server_start():
    logging.info(f"Serwer uruchomiony. Autor: {AUTHOR_NAME}. Port: {TCP_PORT}")


# Funkcja do uzyskania strefy czasowej na podstawie adresu IP
def get_timezone_from_ip(ip_address):
    try:
        # Jeśli klient to localhost, ustaw strefę czasową ręcznie
        if ip_address in ["127.0.0.1", "::1"]:
            logging.info("Lokalny klient. Ustawienie domyślnej strefy czasowej na Europe/Warsaw.")
            return "Europe/Warsaw"

        response = requests.get(f"https://ipapi.co/{ip_address}/timezone")
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        logging.error(f"Nie udało się pobrać strefy czasowej dla IP {ip_address}: {e}")
    return "UTC"  # Domyślna strefa czasowa


# Inicjalizacja aplikacji Flask
app = Flask(__name__)


@app.route("/")
def index():
    # Pobranie adresu IP klienta
    client_ip = request.remote_addr
    timezone = get_timezone_from_ip(client_ip)
    now_utc = datetime.now(pytz.utc)

    # Konwersja czasu do strefy czasowej klienta
    try:
        client_tz = pytz.timezone(timezone)
        client_time = now_utc.astimezone(client_tz)
    except Exception as e:
        logging.error(f"Nie udało się skonwertować czasu dla IP {client_ip}: {e}")
        client_time = now_utc

    # Generowanie strony HTML
    html_content = f"""
    <html>
    <head><title>Informacje o kliencie</title></head>
    <body>
        <h1>Informacje o kliencie</h1>
        <p>Adres IP klienta: {client_ip}</p>
        <p>Strefa czasowa: {timezone}</p>
        <p>Data i godzina w strefie czasowej klienta: {client_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    log_server_start()
    app.run(host="0.0.0.0", port=TCP_PORT)
