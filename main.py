import requests
from bs4 import BeautifulSoup
import os
import random
import time

# --- CONFIGURAZIONE ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TAG_AFFILIATO = "ikiller-21"  # Sostituisci questo con il tuo Tag ID reale!

# User-Agent per mimetizzarsi ed evitare blocchi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
]

def trova_offerte_amazon():
    """Visita la pagina delle offerte lampo e ne estrae una."""
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    # URL della pagina delle Offerte del Giorno / Lampo di Amazon.it
    url = "https://www.amazon.it/deals"
    
    try:
        response = requests.get(url, headers=headers)
        # Se Amazon ci blocca o non risponde, usciamo
        if response.status_code != 200:
            print(f"Bloccato da Amazon (Codice {response.status_code})")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cerchiamo tutti i "card" dei prodotti in offerta. 
        # NOTA: Queste classi CSS cambiano spesso nel 2026.
        carte_prodotti = soup.find_all('div', {'data-testid': 'grid-desktop-card'})
        
        if not carte_prodotti:
            print("Nessun prodotto trovato.")
            return None
        
        # Ne scegliamo uno a caso dalla prima pagina per ora
        carta = random.choice(carte_prodotti)
        
        # --- Estrazione Dati ---
        titolo = carta.find('div', {'class': 'DealContent-module__truncate_xS02A'}).text.strip()
        link_relativo = carta.find('a', {'class': 'a-link-normal'})['href']
        # Creiamo il link affiliato completo
        link_pulito = link_relativo.split('?')[0] # Rimuove parametri traccianti di Amazon
        link_finale = f"https://www.amazon.it{link_pulito}?tag={TAG_AFFILIATO}"
        
        prezzo_nuovo_raw = carta.find('span', {'class': 'a-price-whole'}).text.strip()
        prezzo_vecchio_raw = carta.find('span', {'class': 'a-text-price'}).text.strip()
        
        # Estraiamo l'immagine. Spesso è un'immagine 'lazyloaded'.
        immagine = carta.find('img')['src']
        
        print(f"Trovata offerta: {titolo} a {prezzo_nuovo_raw}€")
        return {
            "titolo": titolo,
            "prezzo_nuovo": prezzo_nuovo_raw,
            "prezzo_vecchio": prezzo_vecchio_raw,
            "link": link_finale,
            "immagine": immagine
        }
        
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
        return None

def invia_offerta(offerta):
    """Invia l'offerta formattata a Telegram."""
    if not offerta: return

    # Pulizia prezzi (Amazon a volte mette centesimi separati)
    p_vecchio_pulito = offerta["prezzo_vecchio"].replace("€","").replace(",",".")
    p_nuovo_pulito = offerta["prezzo_nuovo"].replace("€","").replace(",",".")

    # Gestione Sconto (A volte Amazon non lo dice chiaramente)
    try:
        sconto = int((1 - float(p_nuovo_pulito) / float(p_vecchio_pulito)) * 100)
        sconto_testo = f"📉 Sconto: -{sconto}%"
    except:
        sconto_testo = "📉 *Sconto Rilevato!*"

    testo = (
        f"🚨 **OFFERTA I KILLER RILEVATA!** 🚨\n\n"
        f"📦 *{offerta['titolo']}*\n\n"
        f"❌ Invece di: ~~{offerta['prezzo_vecchio']}~~\n"
        f"✅ **Prezzo: {offerta['prezzo_nuovo']}€**\n"
        f"{sconto_testo}\n\n"
        f"🛒 Disponibile qui: [SITO AMAZON]({offerta['link']})\n"
        f"⚠️ *Affrettati, scade presto*"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    dati = {'chat_id': CHAT_ID, 'caption': testo, 'photo': offerta["immagine"], 'parse_mode': 'MarkdownV2'}
    requests.post(url, data=dati)

if __name__ == "__main__":
    # Il bot cerca un'offerta vera, se la trova la pubblica
    offerta_reale = trova_offerte_amazon()
    if offerta_reale:
        invia_offerta(offerta_reale)
