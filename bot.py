import requests
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EARNKARO_ID = os.getenv("EARNKARO_ID")

def send_to_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Tokens missing!")
        return None
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        return requests.post(url, json=payload).json()
    except Exception as e:
        print(f"Error: {e}")
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
    print("Bot loop running...")
    while True:
        deal_msg = fetch_live_deals()
        send_to_telegram(deal_msg)
        time.sleep(3600)

# Dummy Server to satisfy Render Free Web Service
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
    # Start bot loop in a background thread
    threading.Thread(target=bot_loop, daemon=True).start()
    
    # Start free web server on port Render provides
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    print(f"Server started on port {port}")
    server.serve_forever()
