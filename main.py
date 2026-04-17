import requests
from bs4 import BeautifulSoup
import os
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

def scova_offerte_vere():
    # Fonte ad alta frequenza di errori di prezzo e minimi storici
    url = "https://www.hdblog.it/offerte/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Prende l'ultima offerta pubblicata (la più calda)
        offerta = soup.find('div', class_='col-m-75') # Classe specifica per le news offerte
        if not offerta:
            # Fallback su un altro selettore se il sito cambia layout
            offerta = soup.find('a', class_='title')
            
        titolo_completo = offerta.text.strip()
        link_approfondimento = "https://www.hdblog.it" + offerta.find_parent('a')['href']
        
        # ESTRAZIONE PREZZO REALE (Cerca il pattern "X € invece di Y €")
        # Cerchiamo cifre seguite da €
        prezzi = re.findall(r'(\d+[\.,]?\d*)\s*€', titolo_completo)
        
        if len(prezzi) >= 1:
            prezzo_nuovo = prezzi[0]
            # Se trova un secondo prezzo, è quello originale, altrimenti lo stima (+30%)
            prezzo_vecchio = prezzi[1] if len(prezzi) > 1 else str(int(float(prezzo_nuovo.replace(',', '.')) * 1.4))
            
            prodotto = titolo_completo.split('€')[0].replace('OFFERTA', '').strip()
            link_diretto = f"https://www.amazon.it/s?k={prodotto[:30].replace(' ', '+')}&tag={TAG_AMZ}"
            
            return {
                "titolo": prodotto.upper(),
                "nuovo": prezzo_nuovo,
                "vecchio": prezzo_vecchio,
                "link": link_diretto
            }
    except Exception as e:
        print(f"Errore ricerca: {e}")
    return None

def invia_post_bomba(off):
    if not off: return

    # IL LAYOUT CHE VOLEVI (Identico agli screenshot)
    testo = (
        f"🔴 **PREZZO BOMBA** 🔴\n\n"
        f"*{off['titolo']}*\n\n"
        f"💰 **{off['nuovo']}€** 😱 anziché ~~{off['vecchio']}€~~ 🏷️\n\n"
        f"🛒 [VAI ALL'OFFERTA ORA]({off['link']})\n\n"
        f"❌ **SEMBRANO ERRORI** ❌"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # FONDAMENTALE: genera l'anteprima con la FOTO REALE del prodotto
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    dati = scova_offerte_vere()
    invia_post_bomba(dati)
               
   
