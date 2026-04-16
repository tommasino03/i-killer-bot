import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def test_diretto():
    # Questo invia un messaggio semplicissimo senza foto o link strani
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "Sveglia i Killer! Il bot è vivo. Se leggi questo, il collegamento funziona."
    }
    r = requests.post(url, data=payload)
    print(f"Risposta di Telegram: {r.text}")

if __name__ == "__main__":
    test_diretto()
