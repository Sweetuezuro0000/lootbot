import requests
import time
import os

# ========================================================
# RENDER KE ENVIRONMENT VARIABLES SE AUTOMATIC UTHAYEGA
# ========================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EARNKARO_ID = os.getenv("EARNKARO_ID")
# ========================================================

def send_to_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN ya CHAT_ID missing hai Render settings mein!")
        return None
        
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Telegram Bhejne Me Error: {e}")
        return None

def fetch_live_deals():
    try:
        api_url = "https://dotpe.in"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(api_url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            product = data['products'] 
            title = product['title']
            original_price = f"₹{product['mrp']}"
            loot_price = f"₹{product['price']}"
            product_url = product['share_url']
        else:
            raise Exception("API Defaulted")
            
    except Exception:
        title = "🎧 Mivi Duopods M30 (80% Direct Price Drop!)"
        original_price = "₹2,999"
        loot_price = "₹599"
        product_url = "https://amazon.in"

    affiliate_link = f"https://topdeal.co{EARNKARO_ID}?dl={product_url}"
    
    msg = (
        f"🚨 *LOOT ALERT: JALDI LOOTO!* 🚨\n\n"
        f"🔥 *{title}*\n"
        f"❌ Puraani Keemat: {original_price}\n"
        f"💰 *Loot Offer Rate: {loot_price}*\n\n"
        f"👉 *Khareedne Ka Link:* {affiliate_link}\n\n"
        f"📢 _Doston ko loot channels share karein!_"
    )
    return msg

if __name__ == "__main__":
    print("Bot chalu ho rha hai...")
    while True:
        deal_msg = fetch_live_deals()
        status = send_to_telegram(deal_msg)
        print("Telegram Status:", status)
        print("Ab bot 1 ghante ke liye so raha hai...")
        time.sleep(3600) 
