import requests
from bs4 import BeautifulSoup
import os
import re

def cerca_offerte_vere():
    # Usiamo un sito che scrive il prezzo nel titolo (es. "Sottocosto", "Errore")
    url = "https://www.hdblog.it/offerte/" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Cerchiamo l'ultima offerta pubblicata
        offerta_raw = soup.find('div', class_='title_not_link') # Esempio di classe
        titolo = offerta_raw.text.upper()
        
        # Usiamo le Regex per trovare il simbolo € e il numero vicino
        prezzi = re.findall(r'(\d+[\.,]\d{2})€', titolo)
        
        if prezzi:
            prezzo_reale = prezzi[0]
            return {
                "titolo": titolo,
                "prezzo": prezzo_reale,
                "link": f"https://www.amazon.it/s?k={titolo[:20].replace(' ', '+')}&tag={os.getenv('TAG_AMZ')}"
            }
    except:
        return None
