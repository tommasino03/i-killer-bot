import requests
from bs4 import BeautifulSoup
import os
import re
import json

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

# Fonti varie: Tech, Casa, Errori generici
FONTI = [
    "https://www.tuttotech.net/offerte/feed/",
    "https://www.smartworld.it/offerte/feed",
    "https://www.hdblog.it/offerte/feed/",
    "https://www.punto-informatico.it/offerte/feed/"
]

def invia_telegram(metodo, payload):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    return requests.post(url, json=payload)

def scansiona_e_seleziona():
    database = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in FONTI:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:10]:
                titolo = item.title.text
                prezzi = re.findall(r'(\d+[\.,]?\d*)\s*€', titolo)
                if prezzi:
                    p_nuovo = prezzi[0].replace(',', '.')
                    # Calcoliamo uno sconto aggressivo visibile
                    p_old = float(p_nuovo) * 1.5 
                    
                    clean_title = re.sub(r'OFFERTA|BOMBA|MINIMO|SCONTO|ERRORE', '', titolo, flags=re.I)
                    clean_title = " ".join(clean_title.split()[:6]).upper()
                    
                    database.append({
                        "id": clean_title, # Usato per la memoria
                        "titolo": clean_title,
                        "prezzo": p_nuovo,
                        "prezzo_old": f"{p_old:.0f}",
                        "link": f"https://www.amazon.it/s?k={clean_title.replace(' ', '+')}&tag={TAG_AMZ}"
                    })
        except: continue
    return database

if __name__ == "__main__":
    offerte = scansiona_e_seleziona()
    
    if offerte:
        # Scegliamo un'offerta a caso tra le migliori 5 per variare sempre il canale
        scelta = random.choice(offerte[:5])
        
        testo = (
            f"❌ **SEMBRANO ERRORI** ❌\n\n"
            f"📦 **{scelta['titolo']}**\n\n"
            f"🔴 **{scelta['prezzo']}€** 😱 invece di ~~{scelta['prezzo_old']}€~~ 🏷️\n\n"
            f"🔥 *SCONTO SHOCK - SOLO POCHI PEZZI!*"
        )
        
        # Creazione del BOTTONE PROFESSIONALE
        markup = {
            "inline_keyboard": [[
                {"text": "🛒 ACQUISTA ORA", "url": scelta['link']}
            ]]
        }
        
        payload = {
            "chat_id": CHAT_ID,
            "text": testo,
            "parse_mode": "Markdown",
            "reply_markup": markup,
            "disable_web_page_preview": False
        }
        
        invia_telegram("sendMessage", payload)
   
