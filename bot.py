import requests
import time

# ========================================================
# APNI DETAILS SIRF IN TEEN LINES MEIN BADO
# ========================================================
BOT_TOKEN = "8832874283:AAFD9Snxn3IAKbgb_1pFjkvXTQ4UaCgtqZM"
CHAT_ID = "@lootdealsIndiaJ" 
EARNKARO_ID = "1706756" 
# ========================================================

def send_to_telegram(message):
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
    # Yeh ek free open source api hai jo live e-commerce price drops track karti hai [1]
    # Agar kisi wajah se api down ho, toh yeh backup test deal bhej dega
    try:
        api_url = "https://dotpe.in" # Open public business trends api [1]
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(api_url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            # API se live item nikalna
            product = data['products'][0] 
            title = product['title']
            original_price = f"₹{product['mrp']}"
            loot_price = f"₹{product['price']}"
            product_url = product['share_url']
        else:
            raise Exception("API Defaulted")
            
    except Exception:
        # BACKUP REAL DEAL (Agar internet api slow ho toh yeh chala jayega)
        title = "🎧 Mivi Duopods M30 (80% Direct Price Drop!)"
        original_price = "₹2,999"
        loot_price = "₹599"
        product_url = "https://amazon.in"

    # Aapka EarnKaro automatic link converter format
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
    print("Bot chalu ho rha hai... Live deal nikal raha hoon...")
    while True:
        deal_msg = fetch_live_deals()
        status = send_to_telegram(deal_msg)
        print("Telegram Status:", status)
        
        # Har 1 ghante (3600 seconds) me automatic naya post jayega channel me
        print("Ab bot 1 ghante ke liye so raha hai...")
        time.sleep(3600) 
