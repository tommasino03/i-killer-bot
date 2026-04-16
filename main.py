import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def invio_ignorante():
    print(f"Sto provando a inviare a: {CHAT_ID}")
    # Metodo ultra-compatibile: parametri diretti nell'URL
    testo = "SISTEMA ONLINE - I KILLER SONO PRONTI"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={testo}"
    
    r = requests.get(url) # Usiamo GET invece di POST
    print(f"Risposta Telegram: {r.text}")

if __name__ == "__main__":
    invio_ignorante()
