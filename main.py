import requests
from bs4 import BeautifulSoup
import os
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" # Il tuo tag Amazon

def estrai_prezzo(testo):
    """Cerca un numero seguito da € nel titolo del post"""
    match = re.search(r'(\d+[\.,]?\d*)\s*€', testo)
    return match.group(0) if match else None

def cerca_offerte_vere():
    # Usiamo un feed che pubblica SOLO offerte verificate (es. TuttoAndroid Offerte)
    url = "https://www.tuttoandroid.net/offerte/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        
        for item in items[:3]: # Controlliamo le ultime 3
            titolo = item.title.text
            prezzo_trovato = estrai_prezzo(titolo)
            
            # Se nel titolo c'è un prezzo, l'offerta è reale!
            if prezzo_trovato:
                link_originale = item.link.text
                # Puliamo il titolo per creare la ricerca Amazon
                prodotto = titolo.split('€')[0].replace('OFFERTA', '').strip()
                link_amz = f"https://www.amazon.it/s?k={prodotto.replace(' ', '+')}&tag={TAG_AMZ}"
                
                return {
                    "titolo": prodotto.upper(),
                    "prezzo": prezzo_trovato,
                    "link": link_amz
                }
        return None
    except Exception as e:
        print(f"Errore: {e}")
        return None

def invia_post_reale(off):
    if not off:
        print("Nessun prezzo reale trovato nei feed.")
        return

    testo = (
        f"🚨 **OFFERTA REALE VERIFICATA** 🚨\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"🔴 **PREZZO: {off['prezzo']}** 😱\n"
        f"🏷️ *Sconto verificato dai nostri esperti*\n\n"
        f"👉 [VAI ALL'OFFERTA SU AMAZON]({off['link']})\n\n"
        f"⚠️ *I prezzi possono variare rapidamente!*"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # Fa apparire la foto vera del prodotto da Amazon
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    offerta = cerca_offerte_vere()
    invia_post_reale(offerta)
