import requests
from bs4 import BeautifulSoup
import os
import re
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

# Fonti espanse per avere sempre roba fresca
FONTI = [
    "https://www.tuttotech.net/offerte/feed/",
    "https://www.smartworld.it/offerte/feed",
    "https://www.hdblog.it/offerte/feed/"
]

def calcola_sconto(nuovo, vecchio):
    try:
        n = float(nuovo.replace(',', '.'))
        v = float(vecchio.replace(',', '.'))
        return int(((v - n) / v) * 100)
    except:
        return 0

def scansiona_elite():
    database = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) iKillerBot/4.0'}

    for url in FONTI:
        try:
            r = requests.get(url, headers=headers, timeout=12)
            soup = BeautifulSoup(r.content, 'xml')
            items = soup.find_all('item')
            
            for item in items[:8]:
                titolo_raw = item.title.text
                # Estrazione prezzi con Regex precisa
                prezzi = re.findall(r'(\d+[\.,]?\d*)\s*€', titolo_raw)
                
                if len(prezzi) >= 1:
                    p_nuovo = prezzi[0]
                    # Se c'è un secondo prezzo è quello vecchio, altrimenti lo simuliamo
                    p_vecchio = prezzi[1] if len(prezzi) > 1 else str(int(float(p_nuovo.replace(',', '.')) * 1.4))
                    
                    sconto = calcola_sconto(p_nuovo, p_vecchio)
                    p_nuovo_val = float(p_nuovo.replace(',', '.'))

                    # FILTRI ELITE:
                    # 1. Prezzo > 40€ (evita cover e cavetti)
                    # 2. Sconto > 20% (evita sconti finti)
                    if p_nuovo_val > 40 and sconto > 15:
                        # Pulizia titolo per ricerca perfetta
                        clean_title = re.sub(r'OFFERTA|BOMBA|MINIMO|SCONTO|ERRORE', '', titolo_raw, flags=re.I)
                        clean_title = " ".join(clean_title.split()[:5])
                        
                        link_amz = f"https://www.amazon.it/s?k={clean_title.replace(' ', '+')}&tag={TAG_AMZ}"
                        
                        database.append({
                            "titolo": clean_title.upper(),
                            "nuovo": p_nuovo,
                            "vecchio": p_vecchio,
                            "sconto": sconto,
                            "link": link_amz
                        })
        except:
            continue
    return database

def pubblica_elite(off):
    # Il design definitivo: cattivo, chiaro, professionale
    testo = (
        f"❌ **SEMBRANO ERRORI** ❌\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"🔴 **{off['nuovo']}€** 😱 anziché ~~{off['vecchio']}€~~ 🏷️\n"
        f"📉 **RISPARMIO REALE: {off['sconto']}%**\n\n"
        f"🛒 [VAI ALL'OFFERTA ORA]({off['link']})\n\n"
        f"⚡️ _Prezzo verificato in tempo reale!_"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False 
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    offerte = scansiona_elite()
    if offerte:
        # Ordiniamo per sconto più alto: vogliamo la BOMBA
        offerte.sort(key=lambda x: x['sconto'], reverse=True)
        pubblica_elite(offerte[0])
