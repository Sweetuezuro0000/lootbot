import requests
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EARNKARO_ID = os.getenv("EARNKARO_ID")

def send_to_telegram(message):
    print(f"[DEBUG] Message bhejne ki koshish... Token available: {bool(BOT_TOKEN)}, Chat ID: {CHAT_ID}")
    if not BOT_TOKEN or not CHAT_ID:
        print("[ERROR] Render settings mein BOT_TOKEN ya CHAT_ID missing hai!")
        return None
        
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        print(f"[TELEGRAM RESPONSE LOGS]: {res.text}")
        return res.json()
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def fetch_live_deals():
    title = "🎧 Mivi Duopods M30 (80% Direct Price Drop!)"
    original_price = "₹2,999"
    loot_price = "₹599"
    product_url = "https://amazon.in"
    affiliate_link = f"https://topdeal.co{EARNKARO_ID}?dl={product_url}"
    
    return (
        f"🚨 *LOOT ALERT: JALDI LOOTO!* 🚨\n\n"
        f"🔥 *{title}*\n"
        f"❌ Puraani Keemat: {original_price}\n"
        f"💰 *Loot Offer Rate: {loot_price}*\n\n"
        f"👉 *Khareedne Ka Link:* {affiliate_link}"
    )

def bot_loop():
    print("[DEBUG] Background Bot Loop Shuru Ho Gaya Hai!")
    # Render loop fass na jaye isliye thoda delay dekar chalayenge
    time.sleep(5) 
    while True:
        deal_msg = fetch_live_deals()
        send_to_telegram(deal_msg)
        print("[DEBUG] Bot ab 1 ghante ke liye sleep mode mein jaa raha hai...")
        time.sleep(3600)

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is alive and running safely!")
        
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    # Start bot loop thread
    t = threading.Thread(target=bot_loop, daemon=True)
    t.start()
    
    # Start web server
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    print(f"[SYSTEM] Server started on port {port}")
    server.serve_forever()
