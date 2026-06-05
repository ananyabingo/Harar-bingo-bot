import osimport random
import threading
import time
from telebot import TeleBot, types
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

ADMIN_NUMBER = "0973020314"
BOT_TOKEN = "8850948511:AAHC36oOh7p7Bm_bAZ8sdJw3Cgx5fOeOkTs"
bot = TeleBot(BOT_TOKEN)

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bingo Bot is Running Live!")
    try:
        with TCPServer(("", port), MyHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(e)

threading.Thread(target=run_dummy_server, daemon=True).start()

game_state = {
    "is_started": False,
    "drawn_numbers": [],
    "all_possible_numbers": list(range(1, 76)),
    "players": {},
    "admin_id": None
}

def get_bingo_letter(num):
    if num <= 15: return f"B-{num}"
    elif num <= 30: return f"I-{num}"
    elif num <= 45: return f"N-{num}"
    elif num <= 60: return f"G-{num}"
    else: return f"O-{num}"

def bingo_game_loop(chat_id):
    game_state["is_started"] = True
    game_state["drawn_numbers"] = []
    numbers_pool = game_state["all_possible_numbers"].copy()
    random.shuffle(numbers_pool)
    bot.send_message(chat_id, "🚨 ጨዋታው ተጀምሯል! በየ 10 ሰከንዱ ቁጥሮች ይወጣሉ...")
    time.sleep(2)
    while game_state["is_started"] and numbers_pool:
        current_num = numbers_pool.pop()
        game_state["drawn_numbers"].append(current_num)
        formatted_num = get_bingo_letter(current_num)
        bot.send_message(chat_id, f"🎰 የወጣው ቁጥር፦ ⭐ 【 {formatted_num} 】 ⭐\n\nየወጡት በሙሉ፦ {', '.join([get_bingo_letter(n) for n in game_state['drawn_numbers']])}")
        time.sleep(10)
    if game_state["is_started"]:
        bot.send_message(chat_id, "🏁 ሁሉም ቁጥሮች አልቀዋል! ጨዋታው ተጠናቋል።")
        game_state["is_started"] = False

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if str(message.from_user.id) == ADMIN_NUMBER or message.from_user.username == ADMIN_NUMBER:
        game_state["admin_id"] = user_id
        
    if user_id not in game_state["players"]:
        game_state["players"][user_id] = {"balance": 0, "card": []}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🎮 Play / ተጫወት", "💵 Wallet / ሂሳብ", "💰 Deposit / ብር አስገባ", "🏆 Bingo! / አሸነፍኩ")
    bot.send_message(message.chat.id, f"👋 እንኳን ወደ ቢንጎ ቦት መጡ!\n\n💰 ቀሪ ሂሳብዎ፦ {game_state['players'][user_id]['balance']} ብር\n\nለመጫወት መጀመሪያ አካውንትዎን ይሙሉ ወይም 'Play' ይበሉ!", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "💰 Deposit / ብር አስገባ")
def deposit_request(message):
    info_text = "💵 **አካውንት ለመሙላት**\n\n1. በቴሌብር (Telebirr) ቁጥር `0940403289` ላይ መክፈል የሚፈልጉትን ብር ይላኩ。\n2. የከፈሉበትን **የሂሳብ ማረጋገጫ (Screenshot)** እዚህ ቦት ላይ ይላኩ。\n\nአስተዳዳሪው አይቶ ወዲያውኑ ብር ያዝልዎታል።"
    bot.send_message(message.chat.id, info_text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'text'], func=lambda msg: not msg.text in ["🎮 Play / ተጫወት", "💵 Wallet / ሂሳብ", "💰 Deposit / ብር አስገባ", "🏆 Bingo! / አሸነፍኩ"])
def handle_receipt(message):
    user_id = message.from_user.id
    if game_state["admin_id"]:
        bot.send_message(game_state["admin_id"], f"📩 አዲስ የክፍያ ሪሲፕት ከ User ID: `{user_id}` መጥቷል።\nእባክህ ቼክ አድርገህ ብር ለመጨመር `/add {user_id} መጠን` ብለህ ጻፍ።")
    bot.send_message(message.chat.id, "✅ ሪሲፕትዎ ለአስተዳዳሪ ተልኳል! በአጭር ደቂቃ ውስጥ ይረጋገጣል።")

@bot.message_handler(commands=['add'])
def add_balance(message):
    if message.from_user.id == game_state["admin_id"]:
        try:
            _, target_id, amount = message.text.split()
            target_id = int(target_id)
            amount = int(amount)
            if target_id in game_state["players"]:
                game_state["players"][target_id]["balance"] += amount
                bot.send_message(target_id, f"🎉 ማረጋገጫዎ ጸድቋል! {amount} ብር አካውንትዎ ላይ ተጨምሯል።")
                bot.send_message(message.chat.id, "✅ ብር በተሳካ ሁኔታ ተጨምሯል።")
        except:
            bot.send_message(message.chat.id, "❌ ስህተት! አጻጻፉ፦ /add [user_id] [amount] መሆን አለበት።")

@bot.message_handler(func=lambda msg: msg.text == "🎮 Play / ተጫወት")
def start_game_trigger(message):
    user_id = message.from_user.id
    if game_state["players"][user_id]["balance"] < 10:
        bot.send_message(message.chat.id, "❌ ለመጫወት ቢያንስ 10 ብር ያስፈልግዎታል! እባክህ መጀመሪያ Deposit አድርግ።")
        return
    game_state["players"][user_id]["balance"] -= 10
    user_card = random.sample(range(1, 76), 25)
    game_state["players"][user_id]["card"] = user_card
    card_text = "🎰 **የእርስዎ የቢንጎ ካርታ ቁጥሮች** 🎰\n\n"
    for i in range(0, 25, 5):
        row = user_card[i:i+5]
        card_text += f"| {' | '.join([str(n) for n in row])} |\n"
    bot.send_message(message.chat.id, card_text, parse_mode="Markdown")
    if not game_state["is_started"]:
        threading.Thread(target=bingo_game_loop, args=(message.chat.id,), daemon=True).start()

@bot.message_handler(func=lambda msg: msg.text == "🏆 Bingo! / አሸነፍኩ")
def check_bingo_winner(message):
    user_id = message.from_user.id
    user_card = game_state["players"].get(user_id, {}).get("card", [])
    if not user_card:
        bot.send_message(message.chat.id, "❌ መጀመሪያ ካርታ አልቆረጡም!")
        return
    is_winner = all(num in game_state["drawn_numbers"] for num in user_card[:5])
    if is_winner:
        game_state["is_started"] = False
        game_state["players"][user_id]["balance"] += 500
        bot.send_message(message.chat.id, "🎉🎉 BINGO! 🎉🎉\nእንኳን ደስ አለዎት! የ 500 ብር ቶቶውን አሸንፈዋል!")
    else:
        bot.send_message(message.chat.id, "❌ ገና ነዎት! ቁጥሮችዎ በሙሉ አልወጡም።")

@bot.message_handler(func=lambda msg: msg.text == "💵 Wallet / ሂሳብ")
def check_balance(message):
    user_id = message.from_user.id
    bal = game_state["players"].get(user_id, {}).get("balance", 0)
    bot.send_message(message.chat.id, f"💰 የእርስዎ የአሁን ቀሪ ሂሳብ፦ {bal} ብር ነው።")

bot.infinity_polling()
