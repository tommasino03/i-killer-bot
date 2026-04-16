import requests
from bs4 import BeautifulSoup
import os
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AFFILIATO = "ikiller-21" 

def cerca_offerta():
    url_feed = "https://www.tuttoandroid.net/offerte/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url_feed, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        if not items:
            return None
        item = random.choice(items[:5])
        titolo = item.title.text.upper()
        query = titolo.split('-')[0].split('(')[0].strip()
        link_amazon = f"https://www.amazon.it/s?k={query.replace(' ', '+')}&tag={TAG_AFFILIATO}"
        return {"titolo": titolo, "link": link_amazon}
    except Exception as e:
        print(f"Errore: {e}")
        return None

def invia_post(off):
    if not off:
        print("Nessuna offerta trovata.")
        return
    testo = (
        f"🚨 *OFFERTA KILLER* 🚨\n\n"
        f"📦 *{off['titolo']}*\n\n"
        f"💰 *PREZZO FOLLIA - SCORTE LIMITATE*\n"
        f"📉 Sconto calcolato oltre il 50%\n\n"
        f"🛒 *ACQUISTA QUI:* \n"
        f"{off['link']}\n\n"
        f"⚠️ _Controlla il prezzo prima di pagare!_"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload)
    print(f"Risposta Telegram: {r.text}")

if __name__ == "__main__":
    offerta = cerca_offerta()
    invia_post(offerta)
