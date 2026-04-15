import requests
import os

# GitHub caricherà questi dati in automatico dalle "Secrets"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def invia_offerta(titolo, prezzo_vecchio, prezzo_nuovo, link, immagine):
    sconto = int((1 - float(prezzo_nuovo.replace(',','.')) / float(prezzo_vecchio.replace(',','.'))) * 100)
    
    testo = (
        f"🚨 *OFFERTA I KILLER* 🚨\n\n"
        f"📦 *{titolo}*\n\n"
        f"❌ Invece di: ~~{prezzo_vecchio}€~~\n"
        f"✅ **Prezzo: {prezzo_nuovo}€**\n"
        f"📉 Sconto: -{sconto}%\n\n"
        f"🛒 Acquista qui: [CLICCA QUI]({link})\n"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    dati = {'chat_id': CHAT_ID, 'caption': testo, 'photo': immagine, 'parse_mode': 'MarkdownV2'}
    requests.post(url, data=dati)

if __name__ == "__main__":
    # Per ora facciamo un invio di prova
    invia_offerta("Mouse Gaming", "90.00", "45.00", "https://amzn.to/test", "https://m.media-amazon.com/images/I/7178uS4pT5L._AC_SL1500_.jpg")
