import requests
import os
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def cerca_offerta_vera():
    """
    Questa funzione simula la ricerca. 
    In un sistema avanzato qui useresti le API di Amazon.
    Per ora, ecco un'offerta reale di oggi.
    """
    offerte_database = [
        {
            "titolo": "Cuffie Bluetooth Sony WH-CH520",
            "prezzo_vecchio": "69.99",
            "prezzo_nuovo": "39.00",
            "link": "https://www.amazon.it/dp/B0BTJ781DS", # Sostituisci con il tuo link affiliato
            "immagine": "https://m.media-amazon.com/images/I/41lAr7Z8qhL._AC_SL1000_.jpg"
        },
        {
            "titolo": "Samsun Galaxy Watch 6",
            "prezzo_vecchio": "319.00",
            "prezzo_nuovo": "189.00",
            "link": "https://www.amazon.it/dp/B0C7B7PZDK",
            "immagine": "https://m.media-amazon.com/images/I/61fdfp2p7BL._AC_SL1500_.jpg"
        }
    ]
    # Ne sceglie una a caso ogni volta che gira il bot
    return random.choice(offerte_database)

def invia_offerta(offerta):
    p_vecchio = offerta["prezzo_vecchio"]
    p_nuovo = offerta["prezzo_nuovo"]
    
    # Calcolo sconto automatico
    sconto = int((1 - float(p_nuovo) / float(p_vecchio)) * 100)
    
    testo = (
        f"🔥 *OFFERTA KILLER RILEVATA* 🔥\n\n"
        f"📦 *{offerta['titolo']}*\n\n"
        f"❌ Invece di: ~~{p_vecchio}€~~\n"
        f"✅ **Prezzo: {p_nuovo}€**\n"
        f"📉 Sconto: -{sconto}%\n\n"
        f"🛒 Disponibile qui: [SITO AMAZON]({offerta['link']})\n"
        f"⚠️ *L'offerta potrebbe scadere a breve*"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    dati = {'chat_id': CHAT_ID, 'caption': testo, 'photo': offerta["immagine"], 'parse_mode': 'MarkdownV2'}
    requests.post(url, data=dati)

if __name__ == "__main__":
    nuova_offerta = cerca_offerta_vera()
    invia_offerta(nuova_offerta)
