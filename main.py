import requests
from bs4 import BeautifulSoup
import os
import re
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

# Lista di fonti affidabili per errori di prezzo e sconti tech
FONTI = [
    "https://www.hdblog.it/offerte/",
    "https://www.tuttoandroid.net/offerte/",
    "https://www.smartworld.it/offerte"
]

def estrai_prezzi(testo):
    """Estrae tutti i prezzi da un testo e restituisce il più basso e il più alto"""
    prezzi = re.findall(r'(\d+[\.,]\d{2})', testo)
    if not prezzi:
        prezzi = re.findall(r'(\d+)', testo) # Fallback per numeri senza decimali
    
    numeri = sorted([float(p.replace(',', '.')) for p in prezzi if float(p.replace(',', '.')) > 5])
    
    if len(numeri) >= 2:
        return f"{numeri[0]:.2f}", f"{numeri[-1]:.2f}"
    elif len(numeri) == 1:
        return f"{numeri[0]:.2f}", f"{numeri[0]*1.4:.0f}" # Simula prezzo originale
    return None, None

def scansiona_web():
    offerte_scovate = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) iKillerBot/3.0'}

    for url in FONTI:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Cerca i titoli degli articoli (cambia in base al sito)
            links = soup.find_all(['h2', 'h3', 'a'], limit=15)
            
            for l in links:
                txt = l.text.strip().upper()
                # Filtro "Bomba": pubblica solo se contiene parole forti o un prezzo
                if any(x in txt for x in ["€", "OFFERTA", "MINIMO", "ERRORE", "SCONTO"]):
                    p_nuovo, p_vecchio = estrai_prezzi(txt)
                    
                    if p_nuovo:
                        prodotto = txt.split('€')[0].replace('OFFERTA', '').strip()
                        offerte_scovate.append({
                            "titolo": prodotto[:60],
                            "nuovo": p_nuovo,
                            "vecchio": p_vecchio,
                            "link": f"https://www.amazon.it/s?k={prodotto[:30].replace(' ', '+')}&tag={TAG_AMZ}"
                        })
        except:
            continue
    return offerte_scovate

def invia_killer_post(off):
    # Template grafico identico ai canali top
    testo = (
        f"❌ **SEMBRANO ERRORI** ❌\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"🔴 **{off['nuovo']}€** 😱 anziché ~~{off['vecchio']}€~~ 🏷️\n\n"
        f"🛒 [VAI ALL'OFFERTA ORA]({off['link']})\n\n"
        f"🔥 *PREZZO BOMBA RILEVATO* 🔥"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # Genera la foto reale del prodotto
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    lista = scansiona_web()
    if lista:
        # Sceglie una delle migliori offerte trovate
        invia_killer_post(random.choice(lista))
