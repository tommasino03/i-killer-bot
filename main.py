import requests
from bs4 import BeautifulSoup
import os
import random

# Configurazione Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Metti il tuo Tag Affiliato Amazon qui (es: ikiller-21)
TAG_AFFILIATO = "ikiller-21" 

def genera_dati_killer():
    """Recupera un prodotto e genera prezzi 'Bomba' credibili"""
    url_feed = "https://www.tuttoandroid.net/offerte/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url_feed, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        if not items: return None
        
        item = random.choice(items[:5])
        titolo = item.title.text.upper()
        # Puliamo il titolo per la ricerca Amazon
        query = titolo.split('-')[0].split('(')[0].strip()
        link_amazon = f"https://www.amazon.it/s?k={query.replace(' ', '+')}&tag={TAG_AFFILIATO}"
        
        # --- GENERAZIONE PREZZI SIMULATI (Stile Outlet) ---
        # Creiamo un prezzo vecchio (es. 199-499) e uno nuovo (sconto 60-80%)
        p_vecchio = random.randint(149, 599)
        p_nuovo = int(p_vecchio * random.uniform(0.2, 0.4)) # Sconto del 60-80%
        
        return {
            "titolo": titolo,
            "prezzo_vecchio": f"{p_vecchio},00",
            "prezzo_nuovo": f"{p_nuovo},90",
            "link": link_amazon,
            # Immagine placeholder (poiché non possiamo leggere Amazon)
            "immagine": "https://m.media-amazon.com/images/G/08/social_share/amazon_logo._CB633266945_.png"
        }
    except Exception as e:
        print(f"Errore: {e}")
        return None

def invia_post_scrucio_style(off):
    """Invia il post formattato come gli screenshot"""
    if not off: return

    # Costruiamo il template testuale esattamente come negli screenshot
    testo = (
        f"❌ **SEMBRANO ERRORI** ❌\n\n"
        f"*{off['titolo']}*\n\n"
        f"🔴 **{off['prezzo_nuovo']}€** 😱 anziché ~~{off['prezzo_vecchio']}€~~ 🏷️\n"
        f"[VAI ALL'OFFERTA]({off['link']})"
    )

    # Inviamo con sendPhoto per avere immagine e testo uniti
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": off['immagine'], # Link dell'immagine
        "caption": testo,
        "parse_mode": "Markdown" # Markdown v1 è più stabile
    }
    
    r = requests.post(url, json=payload)
    print(f"Risposta Telegram: {r.text}")

if __name__ == "__main__":
    offerta_dati = genera_dati_killer()
    invia_post_scrucio_style(offerta_dati)
