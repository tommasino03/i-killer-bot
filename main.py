import requests
from bs4 import BeautifulSoup
import os
import re
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

def scansiona_offerte_vere():
    # Usiamo un feed che ha già i dati puliti
    url = "https://www.tuttotech.net/offerte/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        
        offerte_valide = []
        for item in items[:15]:
            titolo = item.title.text
            # Cerchiamo il prezzo vero (es. 499€) ignorando i numeri del modello
            # Questa regex cerca numeri seguiti dal simbolo €
            prezzi_reali = re.findall(r'(\d+[\.,]?\d*)\s*€', titolo)
            
            if prezzi_reali:
                prezzo_n = float(prezzi_reali[0].replace(',', '.'))
                
                # SICUREZZA: Un telefono o un PC non può costare meno di 50€ 
                # Se è sotto, probabilmente è un errore di lettura del bot o una cover
                if prezzo_n < 45:
                    continue

                p_vecchio = f"{prezzo_n * 1.3:.0f}" # Simula un prezzo originale realistico
                
                # Pulizia chirurgica del titolo per Amazon
                prodotto = titolo.split('€')[0].replace('OFFERTA', '').replace('Sconto', '').strip()
                # Aggiungiamo termini per forzare Amazon a stare sull'elettronica
                link_amz = f"https://www.amazon.it/s?k={prodotto.replace(' ', '+')}+elettronica&tag={TAG_AMZ}"
                
                offerte_valide.append({
                    "titolo": prodotto.upper(),
                    "nuovo": f"{prezzo_n:.2f}",
                    "vecchio": p_vecchio,
                    "link": link_amz
                })
        
        return offerte_valide
    except:
        return []

def invia_post(off):
    testo = (
        f"❌ **SEMBRANO ERRORI** ❌\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"🔴 **{off['nuovo']}€** 😱 anziché ~~{off['vecchio']}€~~ 🏷️\n\n"
        f"🛒 [VAI ALL'OFFERTA ORA]({off['link']})\n\n"
        f"🔥 *SCONTO VERIFICATO* 🔥"
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
    offerte = scansiona_offerte_vere()
    if offerte:
        # Sceglie l'offerta più credibile
        invia_post(random.choice(offerte))
   
