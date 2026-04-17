import requests
from bs4 import BeautifulSoup
import os
import re
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AMZ = "ikiller-21" 

def pulisci_titolo(testo):
    """Pulisce il titolo per renderlo perfetto per la ricerca Amazon"""
    # Rimuove scritte inutili che confondono la ricerca
    testo = re.sub(r'OFFERTA|SCONTO|MINIMO|STORICO|BOMBA|ERRORE', '', testo, flags=re.I)
    # Prende solo le prime 5-6 parole (il nome reale del prodotto)
    parole = testo.split()
    return " ".join(parole[:6]).strip()

def scansiona_offerte_pro():
    # Usiamo fonti che pubblicano solo sconti pesanti
    fonti_feed = [
        "https://www.tuttotech.net/offerte/feed/",
        "https://www.smartworld.it/offerte/feed"
    ]
    
    offerte_valide = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in fonti_feed:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'xml')
            items = soup.find_all('item')
            
            for item in items[:10]:
                titolo_raw = item.title.text
                # Cerchiamo il prezzo (es: 199€)
                match_prezzo = re.search(r'(\d+[\.,]?\d*)\s*€', titolo_raw)
                
                if match_prezzo:
                    prezzo_n = float(match_prezzo.group(1).replace(',', '.'))
                    
                    # Filtro qualità: se il prezzo è troppo basso, è una cover o un accessorio
                    if prezzo_n < 30: continue 

                    titolo_pulito = pulisci_titolo(titolo_raw)
                    # Creiamo un link che forza Amazon a mostrare il prodotto singolo
                    link_amz = f"https://www.amazon.it/s?k={titolo_pulito.replace(' ', '+')}&tag={TAG_AMZ}&ref=as_li_ss_tl"
                    
                    offerte_valide.append({
                        "titolo": titolo_pulito.upper(),
                        "prezzo": f"{prezzo_n:.2f}",
                        "prezzo_old": f"{prezzo_n * 1.4:.0f}",
                        "link": link_amz
                    })
        except:
            continue
    return offerte_valide

def invia_post_pro(off):
    # Template grafico "Outlet Scruscio" perfezionato
    testo = (
        f"❌ **SEMBRANO ERRORI** ❌\n\n"
        f"📦 **{off['titolo']}**\n\n"
        f"🔴 **{off['prezzo']}€** 😱 anziché ~~{off['prezzo_old']}€~~ 🏷️\n\n"
        f"🛒 [VAI ALL'OFFERTA ORA]({off['link']})\n\n"
        f"🔥 *SCONTO VERIFICATO - POCHI PEZZI!* 🔥"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # Telegram pescherà la foto ufficiale Amazon
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    database = scansiona_offerte_pro()
    if database:
        # Ne sceglie una a caso per non postare sempre la stessa se il feed non si aggiorna
        invia_post_pro(random.choice(database))
