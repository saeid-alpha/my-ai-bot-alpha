import os
import asyncio
import aiohttp
from flask import Flask
from threading import Thread
from gtts import gTTS
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- FLASK SERVER (For Render Port) ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Saeid Alpha AI V9.0 is Live & Stable! 💎"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- CONFIG & DATABASE ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
ADMIN_ID = 6363842144 # আপনার চ্যাট আইডি এখানে দিন (Broadcasting এর জন্য)
BANNER_URL = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"

user_memory = defaultdict(list)
all_users = set() # সব ইউজারের আইডি সেভ রাখার জন্য (Broadcast এর জন্য)

# --- PREMIUM UI KEYBOARDS ---
def main_menu():
    kb = [[KeyboardButton("🛠 প্রিমিয়াম টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI Mode"), KeyboardButton("🌦️ ওয়েদার ও টাইম")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def toolbox_ui():
    buttons = [
        [InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data="t_img"),
         InlineKeyboardButton("🌐 অল ট্রান্সলেটর", callback_data="t_trans")],
        [InlineKeyboardButton("🎙 Text to Voice", callback_data="t_ttv"),
         InlineKeyboardButton("🎧 Voice to Text", callback_data="t_vtt")],
        [InlineKeyboardButton("💰 কারেন্সি কনভার্টার", callback_data="t_curr"),
         InlineKeyboardButton("🔗 URL শর্টেনার", callback_data="t_url")],
        [InlineKeyboardButton("❌ মেনু বন্ধ করুন", callback_data="close")]
    ]
    return InlineKeyboardMarkup(buttons)

# --- CORE FUNCTIONS ---

async def safe_api_call(func, *args, **kwargs):
    """এরর হ্যান্ডলিং যাতে বট ক্রাশ না করে।"""
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        return None

async def get_ai_response(user_id, user_name, text):
    system_prompt = f"You are Saeid Alpha AI 👑 (Saeid). High Intellect. User: {user_name}."
    history = user_memory[user_id][-5:]
    payload = {"messages": [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": text}]}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=20) as resp:
            data = await resp.json()
            reply = data.get("response", "সার্ভার ব্যস্ত আছে।")
            user_memory[user_id].append({"role": "user", "content": text})
            user_memory[user_id].append({"role": "assistant", "content": reply})
            return reply

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    
    welcome = (f"💎 <b>SAEID ALPHA AI | V9.0</b> 💎\n{'-'*25}\n"
               f"স্বাগতম <b>{user.first_name}</b>!\n"
               f"আমি একটি অল-ইন-ওয়ান এআই বট। আপনার সকল প্রয়োজনীয় টুলস এখানে সাজানো আছে।")
    
    await update.message.reply_photo(BANNER_URL, caption=welcome, reply_markup=main_menu(), parse_mode=ParseMode.HTML)

# --- GROUP WELCOME MESSAGE ---
async def welcome_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🌟 স্বাগতম {member.first_name} আমাদের গ্রুপে! আমি Saeid Alpha AI, আপনাদের সেবায় নিয়োজিত। 👑")

# --- ADMIN BROADCAST (Alert All Users) ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return await update.message.reply_text("ব্যবহার: `/alert আপনার মেসেজ`")
    
    count = 0
    for user_id in all_users:
        try:
            await context.bot.send_message(user_id, f"📢 <b>SAEID ALPHA ALERT:</b>\n\n{msg}", parse_mode=ParseMode.HTML)
            count += 1
        except: continue
    await update.message.reply_text(f"✅ {count} জন ইউজারের কাছে এলার্ট পাঠানো হয়েছে।")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "🛠 প্রিমিয়াম টুলবক্স":
        return await update.message.reply_text("💎 <b>সিলেক্ট করুন আপনার টুল:</b>", reply_markup=toolbox_ui(), parse_mode=ParseMode.HTML)

    if text == "👤 প্রোফাইল":
        info = (f"👤 <b>User Info</b>\n🆔 ID: <code>{user.id}</code>\n👤 User: @{user.username}\n🏆 Rank: <b>Elite</b>")
        return await update.message.reply_text(info, parse_mode=ParseMode.HTML)

    if text == "🌦️ ওয়েদার ও টাইম":
        now = datetime.now().strftime("%I:%M %p | %d %b %Y")
        return await update.message.reply_text(f"⏰ <b>বর্তমান সময়:</b> {now}\n🌦️ ওয়েদার চেক করতে আপনার শহরের নাম লিখুন।", parse_mode=ParseMode.HTML)

    # General AI Chat
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await safe_api_call(get_ai_response, user.id, user.first_name, text)
    await update.message.reply_text(f"👑 <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN ---
if __name__ == "__main__":
    if TELEGRAM_TOKEN:
        Thread(target=run_flask).start()
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("alert", broadcast))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_group))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        app.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer("শীঘ্রই এটি চালু হচ্ছে!")))
        
        print("Saeid Alpha V9.0 is Running with Admin Alerts! 🚀")
        app.run_polling(drop_pending_updates=True)
