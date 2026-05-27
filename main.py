import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import telebot
from telebot import types

# Render ፖርት እንዲያገኝ የሚያደርግ አጭር ሰርቨር
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ሰርቨሩን በጀርባ እንዲሰራ ያደርጋል
threading.Thread(target=run_health_check, daemon=True).start()

# --- 1. አዲሱ ትክክለኛ የቦት ቶከን እዚህ ተስተካክሏል ---
API_TOKEN = '8850948511:AAHC36oOh7p7Bm_bAZ8sdJw3Cgx5fOeOkTs'
bot = telebot.TeleBot(API_TOKEN)

bot.delete_webhook()

# --- 2. የእርስዎ ትክክለኛ የቢንጎ ጨዋታ ሊንክ እዚህ ተስተካክሏል ---
WEBAPP_URL = "https://tiiny.site"

# የቦቱ አዝራሮች (Commands) በአማርኛ
def set_bot_commands():
    commands = [
        types.BotCommand("start", "ቦቱን ለመቀስቀስ / አስጀምር"),
        types.BotCommand("register", "ለመመዝገብ"),
        types.BotCommand("play", "ቢንጎ ለመጫወት"),
        types.BotCommand("deposit", "ብር ለማስገባት"),
    ]
    bot.set_my_commands(commands)

set_bot_commands()

# የ /start ትዕዛዝ ሲላክ የሚመጣ መልስ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # --- 3. የእርስዎ የቴሌብር ስልክ ቁጥሮች እዚህ ተስተካክለዋል ---
    owner_name = "የእርስዎ ስም"
    account_1 = "0940403289"
    account_2 = "0979152240"
    
    telegram_id = message.from_user.id
    
    welcome_text = (
        f"እንኳን ወደ ሀረር ቢንጎ በደህና መጡ! 🎰\n\n"
        f"👤 የባንክ አካውንት ባለቤት ስም፦ {owner_name}\n\n"
        f"💳 በቴሌብር (Telebirr) ገንዘብ ለማስገባት፦\n"
        f"የጨዋታ መግቢያ ክፍያዎን ወደ አንደኛው ቁጥር ይላኩ፦\n"
        f"የአካውንት ቁጥር 1፦ {account_1}\n"
        f"የአካውንት ቁጥር 2፦ {account_2}\n\n"
        f"⚠️ በጣም አስፈላጊ፦ ገንዘብ ሲልኩ በማስተወሻ (Reason/Remark) ቦታ ላይ "
        f"ይህንን የእርስዎን የቴሌግራም መታወቂያ ቁጥር [{telegram_id}] የግድ ማስገባት አለብዎት!\n\n"
        f"ገንዘብ ከላኩ በኋላ መጫወት ለመጀመር ከታች ያለውን 'ተጫወት 🎰' የሚለውን ይጫኑ።"
    )
    
    # የመጫወቻ ኪቦርድ አዝራሮች በአማርኛ
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # የዌብቪው (WebView) ጨዋታ መክፈቻ ቁልፍ
    webapp_info = types.WebAppInfo(url=WEBAPP_URL)
    play_btn = types.KeyboardButton(text="ተጫወት 🎰", web_app=webapp_info)
    register_btn = types.KeyboardButton(text="ተመዝገብ 📝")
    
    balance_btn = types.KeyboardButton(text="ሒሳብ አሳይ 💵")
    deposit_btn = types.KeyboardButton(text="ብር አስገባ 💰")
    
    support_btn = types.KeyboardButton(text="እርዳታ ☎️")
    instruction_btn = types.KeyboardButton(text="መመሪያ 📖")
    
    transfer_btn = types.KeyboardButton(text="ብር አጋራ 🔁")
    withdraw_btn = types.KeyboardButton(text="ብር አውጣ 🤑")
    
    invite_btn = types.KeyboardButton(text="ጋብዝ 🔗")
    bonus_btn = types.KeyboardButton(text="ቦነስ ቀይር 💎")
    
    markup.add(play_btn, register_btn)
    markup.add(balance_btn, deposit_btn)
    markup.add(support_btn, instruction_btn)
    markup.add(transfer_btn, withdraw_btn)
    markup.add(invite_btn, bonus_btn)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# ቦቱን ማለቂያ በሌለው ሉፕ ማሰራት
if __name__ == "__main__":
    bot.polling(none_stop=True)
