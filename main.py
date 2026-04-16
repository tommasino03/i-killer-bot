import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def debug_bot():
    print("--- INIZIO DEBUG ---")
    # Verifichiamo se le variabili esistono
    if not TOKEN: 
        print("ERRORE: La Secret TELEGRAM_TOKEN è vuota!")
        return
    if not CHAT_ID:
        print("ERRORE: La Secret TELEGRAM_CHAT_ID è vuota!")
        return

    # Stampiamo solo i primi e ultimi caratteri per sicurezza
    print(f"Token caricato: {TOKEN[:5]}...{TOKEN[-5:]}")
    print(f"Chat ID caricato: {CHAT_ID}")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "Test Finale i Killer"}
    
    r = requests.post(url, json=payload)
    print(f"Risposta completa di Telegram: {r.text}")
    print("--- FINE DEBUG ---")

if __name__ == "__main__":
    debug_bot()
