import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def test_connessione():
    if not TOKEN or not CHAT_ID:
        print("❌ ERRORE: Token o Chat ID mancanti nelle Secrets di GitHub!")
        return

    print(f"Tentativo di invio a: {CHAT_ID}")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🎯 **i KILLER TEST** 🎯\nSe leggi questo, il bot è configurato correttamente!"
    }
    
    try:
        r = requests.post(url, json=payload)
        risultato = r.json()
        if risultato.get("ok"):
            print("✅ SUCCESSO! Il messaggio è arrivato su Telegram.")
        else:
            print(f"❌ ERRORE DA TELEGRAM: {risultato.get('description')}")
            print(f"Codice errore: {risultato.get('error_code')}")
    except Exception as e:
        print(f"❌ ERRORE DI RETE: {e}")

if __name__ == "__main__":
    test_connessione()
