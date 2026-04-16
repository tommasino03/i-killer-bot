import requests
from bs4 import BeautifulSoup
import os
import random

# Configurazione Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Sostituisci questo con il tuo tag appena Amazon ti approva (es: ikiller-21)
TAG_AFFILIATO = "ikiller-21" 

def estrai_offerte():
    """Legge le ultime offerte tech da un feed affidabile"""
    url = "https://www.tuttoandroid.net/offerte/feed/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) iKillerBot/1.0'}
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        
        offerte = []
        for item in items[:5]: # Prende le ultime 5 per sicurezza
            titolo = item.title.text
            link = item.link.text
            # Se il link è un redirect o un sito tech, creiamo la ricerca su Amazon
            link_amazon = f"https://www.amazon.it/s?k={titolo.replace(' ', '+')}&tag={TAG_AFFILIATO}"
            
            offerte.append({
                "titolo": titolo,
                "link": link_amazon
            })
        return offerte
    except Exception as e:
        print(f"Errore estrazione: {e}")
        return []

def pubblica_offerta(offerta):
    """Invia l'offerta con una formattazione Killer"""
    testo = (
        f"🔥 **OFFERTA KILLER RILEVATA** 🔥\n\n"
        f"📦 **{offerta['titolo']}**\n\n"
        f"💰 Verifica il prezzo e la disponibilità qui:\n"
        f"🛒 [VEDI SU AMAZON]({offerta['link']})\n\n"
        f"📢 _Notifiche attive per non perdere i minimi storici!_"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": testo, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # Mostra l'anteprima del link (foto)
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    lista_offerte = estrai_offerte()
    if lista_offerte:
        # Ne sceglie una a caso tra le ultime per non postare sempre la stessa
        scelta = random.choice(lista_offerte)
        pubblica_offerta(scelta)
        print(f"Offerta pubblicata: {scelta['titolo']}")
    else:
        print("Nessuna offerta trovata in questo turno.")
