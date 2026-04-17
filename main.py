import requests
from bs4 import BeautifulSoup
import os
import re
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

def scansiona_offerte_top():
    fonti = [
        "https://www.tuttotech.net/offerte/feed/",
        "https://www.smartworld.it/offerte/feed",
        "https://www.hdblog.it/offerte/feed/"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    offerte = []

    for url in fonti:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:10]:
                titolo = item.title.text
                link_art = item.link.text
                
                # Cerchiamo il prezzo
                prezzi = re.findall(r'(\d+[\.,]?\d*)\s*€', titolo)
                if prezzi:
                    p_nuovo = float(prezzi[0].replace(',', '.'))
                    if p_nuovo < 20: continue # Filtro qualità
                    
                    p_old = f"{p_nuovo * 1.5:.0f}"
                    
                    # Estrazione immagine dall'articolo (il tocco magico)
                    img_url = "https://i.imgur.com/8N7V9D0.png" # Default
                    try:
                        r_img = requests.get(link_art, headers=headers, timeout=5)
                        s_img = BeautifulSoup(r_img.text, 'html.parser')
                        meta_img = s_img.find("meta", property="og:image")
                        if meta_img: img_url = meta_img["content"]
                    except: pass

                    clean_title = re.sub(r'OFFERTA|BOMBA|MINIMO|SCONTO|ERRORE', '', titolo, flags=re.I)
                    clean_title = " ".join(clean_title.split()[:7]).upper()
                    
                    link_final = f"https://www.amazon.it/s?k={clean_title.replace(' ', '+')}&tag={TAG_AMZ}"
                    
                    offerte.append({
                        "titolo": clean_title,
                        "nuovo": f"{p_nuovo:.2f}",
                        "vecchio": p_old,
                        "img": img_url,
                        "link": link_final
                    })
        except: continue
    return offerte

def pubblica_top(off):
    # TEMPLATE IDENTICO AI CANALI TOP
    testo = (
        f"🔴 **PREZZO SHOCK** 🔴\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"💰 **{off['nuovo']}€** 😱 invece di ~~{off['vecchio']}€~~ 🏷️\n\n"
        f"❌ **SEMBRANO ERRORI** ❌\n"
        f"⚠️ *POCHI PEZZI DISPONIBILI!*"
    )

    # CREAZIONE BOTTONE INLINE
    reply_markup = {
        "inline_keyboard": [[
            {"text": "🛒 VAI ALL'OFFERTA ORA", "url": off['link']}
        ]]
    }

    # Invio della FOTO con didascalia e bottone
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": off['img'],
        "caption": testo,
        "parse_mode": "Markdown",
        "reply_markup": reply_markup
    }
    
    r = requests.post(url, json=payload)
    print(f"Risultato: {r.text}")

if __name__ == "__main__":
    offerte = scansiona_offerte_top()
    if offerte:
        pubblica_top(random.choice(offerte))
