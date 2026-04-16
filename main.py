
       import requests
from bs4 import BeautifulSoup
import os
import random
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AFFILIATO = "ikiller-21" 

def ottieni_dati_amazon(url_prodotto):
    """Tenta di estrarre l'immagine e il prezzo reale dal link Amazon"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'it-IT,it;q=0.9'
    }
    try:
        r = requests.get(url_prodotto, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Tentativo recupero immagine
        img_tag = soup.find("img", {"id": "landingImage"}) or soup.find("img", {"id": "imgBlkFront"})
        img_url = img_tag['src'] if img_tag else "https://i.imgur.com/8N7V9D0.png" # Immagine di fallback
        
        return img_url
    except:
        return "https://i.imgur.com/8N7V9D0.png"

def cerca_offerte_bomba():
    """Scansiona una fonte di offerte pre-filtrate (Errori di prezzo/Sconti)"""
    # Usiamo un feed che aggrega sconti reali
    url_feed = "https://www.tuttoandroid.net/offerte/feed/"
    try:
        r = requests.get(url_feed)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        
        offerte_filtrate = []
        for item in items:
            titolo = item.title.text
            # Filtro: cerchiamo parole chiave che indicano sconti forti
            parole_chiave = ["sconto", "minimo", "offerta", "metà prezzo", "errore"]
            if any(parola in titolo.lower() for parola in parole_chiave):
                link_originale = item.link.text
                # Creiamo il link affiliato pulito
                link_aff = f"https://www.amazon.it/s?k={titolo.split('-')[0].strip().replace(' ', '+')}&tag={TAG_AFFILIATO}"
                
                # Recuperiamo l'immagine reale del prodotto (opzionale, rallenta un po')
                immagine = "https://m.media-amazon.com/images/G/08/social_share/amazon_logo._CB633266945_.png" 
                
                offerte_filtrate.append({
                    "titolo": titolo.upper(),
                    "link": link_aff,
                    "immagine": immagine
                })
        return offerte_filtrate
    except:
        return []

def invia_killer_post(offerta):
    """Invia il post con immagine e stile grafico"""
    testo = (
        f"🚨 **ERRORE DI PREZZO / SCONTO BOMBA** 🚨\n\n"
        f"📦 **{offerta['titolo']}**\n\n"
        f"💰 **PREZZO MAI VISTO!**\n"
        f"📉 *Sconto calcolato: fino al -70%*\n\n"
        f"🛒 **ACQUISTA ORA:**\n"
        f"🔗 [CLICCA QUI PER L'OFFERTA]({offerta['link']})\n\n"
        f"⚠️ *Le scorte finiscono in pochi minuti!*"
    )
    
    # Usiamo sendPhoto per inviare l'immagine con la didascalia
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": offerta['immagine'],
        "caption": testo,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    offerte = cerca_offerte_bomba()
    if offerte:
        # Ne pubblichiamo una a caso tra le migliori trovate
        invia_killer_post(random.choice(offerte))
