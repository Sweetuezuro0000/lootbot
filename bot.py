import requests
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys

def log(message):
    print(message)
    sys.stdout.flush()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EARNKARO_ID = os.getenv("EARNKARO_ID")

def send_to_telegram(message):
    log(f"[DEBUG] Sending request with Chat ID: {CHAT_ID}")
    if not BOT_TOKEN or not CHAT_ID:
        log("[ERROR] Settings missing in Render variables!")
        return None
        
    # Strictly clean, pure official Telegram URL formulation
    # Zero dependency on string appending bugs
    token_clean = str(BOT_TOKEN).strip()
    url = f"https://api.telegram.org{token_clean}/sendMessage"
    
    payload = {
        "chat_id": str(CHAT_ID).strip(), 
        "text": message, 
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        res = requests.post(url, json=payload, timeout=12)
        log(f"[TELEGRAM API OUTPUT]: {res.text}")
        return res.json()
    except Exception as e:
        log(f"[ERROR] API Request failed: {e}")
        return None

def fetch_live_deals():
    title = "🎧 Mivi Duopods M30 (80% Direct Price Drop!)"
    original_price = "₹2,999"
    loot_price = "₹599"
    product_url = "https://amazon.in"
    affiliate_link = f"https://topdeal.co{EARNKARO_ID}?dl={product_url}"
    
    return (
        f"🚨 <b>LOOT ALERT: JALDI LOOTO!</b> 🚨\n\n"
        f"🔥 <b>{title}</b>\n"
        f"❌ Puraani Keemat: {original_price}\n"
        f"💰 <b>Loot Offer Rate: {loot_price}</b>\n\n"
        f"👉 <a href='{affiliate_link}'><b>Khareedne Ka Link Click Karein</b></a>"
    )

def bot_loop():
    log("[SYSTEM-START] Background Thread Bot Loop Initialized!")
    time.sleep(3)
    while True:
        deal_msg = fetch_live_deals()
        send_to_telegram(deal_msg)
        log("[SLEEP] Bot entering resting loop cycle...")
        time.sleep(3600)

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot system is alive and operational!")
        
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    t = threading.Thread(target=bot_loop, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    log(f"[SYSTEM] Web network server mounted on port: {port}")
    server.serve_forever()
