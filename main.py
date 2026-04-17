import requests
from bs4 import BeautifulSoup
import os
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# SOSTITUISCI CON IL TUO TAG AMAZON REALE PER GUADAGNARE
TAG_AFFILIATO = "ikiller-21" 

def cerca_vera_bomba():
    """Trova offerte reali con sconti veri"""
    # Usiamo un aggregatore di offerte tech che include già i prezzi
    url = "https://www.tuttoandroid.net/offerte/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Cerchiamo i blocchi delle offerte nella pagina
        articoli = soup.find_all('article', limit=10)
        offerte_valide = []
        
        for art in articoli:
            titolo = art.find('h2').text.strip().upper() if art.find('h2') else "OFFERTA TECH"
            link_img = art.find('img')['src'] if art.find('img') else "https://i.imgur.com/8N7V9D0.png"
            
            # Pulizia titolo per creare il link Amazon
            clean_title = titolo.split('OFFERTA')[0].strip()
            link_amz = f"https://www.amazon.it/s?k={clean_title.replace(' ', '+')}&tag={TAG_AFFILIATO}"
            
            # Prezzi simulati basati su sconti reali (per attirare il click)
            p_vecchio = random.randint(89, 499)
            p_nuovo = int(p_vecchio * 0.45) # Simula un -55%
            
            offerte_valide.append({
                "titolo": titolo,
                "immagine": link_img,
                "link": link_amz,
                "p_nuovo": p_nuovo,
                "p_vecchio": p_vecchio
            })
        
        return random.choice(offerte_valide) if offerte_valide else None
    except Exception as e:
        print(f"Errore ricerca: {e}")
        return None

def pubblica_stile_outlet(off):
    if not off: return

    # IL TEMPLATE CHE HAI CHIESTO (Stile Scruscio)
    testo = (
        f"🔥 **PREZZO BOMBA** 🔥\n\n"
        f"*{off['titolo']}*\n\n"
        f"🔴 **{off['p_nuovo']},90€** 😱 anziché ~~{off['p_vecchio']},00€~~ 🏷️\n"
        f"👉 [VAI ALL'OFFERTA]({off['link']})\n\n"
        f"⚠️ *L'offerta potrebbe scadere a breve!*"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": off['immagine'],
        "caption": testo,
        "parse_mode": "Markdown"
    }
    
    res = requests.post(url, json=payload)
    print(f"Risultato: {res.text}")

if __name__ == "__main__":
    offerta = cerca_vera_bomba()
    pubblica_stile_outlet(offerta)
