import os
import asyncio
import aiohttp
import requests
from flask import Flask
from threading import Thread
from gtts import gTTS
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- FLASK SERVER (Render Port Binding & Cron-job Fix) ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    # ক্রন-জব এরর (output too large) এড়াতে ছোট রেসপন্স
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
ADMIN_ID = 6363842144 # আপনার চ্যাট আইডি
BANNER_URL = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"

user_memory = defaultdict(list)
all_users = set()

# --- KEYBOARDS ---
def main_menu():
    kb = [[KeyboardButton("🛠 টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI Mode"), KeyboardButton("🌦️ ওয়েদার")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def toolbox_ui():
    buttons = [
        [InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data="t_img"),
         InlineKeyboardButton("🌐 ট্রান্সলেটর", callback_data="t_trans")],
        [InlineKeyboardButton("🎙 Text to Voice", callback_data="t_ttv"),
         InlineKeyboardButton("🎧 Voice to Text", callback_data="t_vtt")],
        [InlineKeyboardButton("💰 কারেন্সি", callback_data="t_curr"),
         InlineKeyboardButton("🔗 URL শর্টেনার", callback_data="t_url")],
        [InlineKeyboardButton("❌ বন্ধ করুন", callback_data="close")]
    ]
    return InlineKeyboardMarkup(buttons)

# --- CORE FUNCTIONS ---
async def get_ai_response(user_id, user_name, text):
    """মেমোরি সেভ রাখা এবং আইডেন্টিটি বজায় রাখা"""
    system_prompt = f"You are Saeid Alpha AI 👑 (Saeid). Platform: Telegram. User: {user_name}."
    history = user_memory[user_id][-5:]
    payload = {"messages": [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": text}]}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=20) as resp:
                data = await resp.json()
                reply = data.get("response", "সার্ভার ব্যস্ত আছে।")
                user_memory[user_id].append({"role": "user", "content": text})
                user_memory[user_id].append({"role": "assistant", "content": reply})
                return reply
        except: return "❌ এপিআই সংযোগ এরর!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    welcome = (f"👑 <b>Saeid Alpha AI V10.0</b>\n"
               f"━━━━━━━━━━━━━━━━━━━━━\n"
               f"স্বাগতম <b>{user.first_name}</b>!\n"
               f"আমি আপনার সব টুলস এবং চ্যাট মেমোরি সহ এখন লাইভ।")
    await update.message.reply_photo(BANNER_URL, caption=welcome, reply_markup=main_menu(), parse_mode=ParseMode.HTML)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info = (f"👤 <b>ইউজার প্রোফাইল</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"User: @{user.username if user.username else 'N/A'}\n"
            f"Rank: <b>PREMIUM GOLD</b> 👑")
    await update.message.reply_text(info, parse_mode=ParseMode.HTML)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """সবাইকে এলার্ট পাঠানো (শুধুমাত্র এডমিন)"""
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return await update.message.reply_text("ব্যবহার: `/alert আপনার মেসেজ`")
    for u_id in all_users:
        try: await context.bot.send_message(u_id, f"📢 <b>SAEID ALPHA ALERT:</b>\n\n{msg}", parse_mode=ParseMode.HTML)
        except: continue
    await update.message.reply_text("✅ এলার্ট পাঠানো সফল হয়েছে।")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    if text == "🛠 টুলবক্স":
        return await update.message.reply_text("💎 <b>প্রিমিয়াম টুলস:</b>", reply_markup=toolbox_ui(), parse_mode=ParseMode.HTML)
    if text == "👤 প্রোফাইল":
        return await profile_handler(update, context)
    
    # AI Chat with Memory
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    await update.message.reply_text(f"👑 <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN RUNNER (Render Fix) ---
if __name__ == "__main__":
    if TELEGRAM_TOKEN:
        Thread(target=run_flask).start() # Flask Port Binding
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # হ্যান্ডলার যোগ করা
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("alert", broadcast))
        app.add_handler(CommandHandler("profile", profile_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        app.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer("শীঘ্রই সব টুল পুরোপুরি চালু হচ্ছে!")))
        
        print(f"Saeid Alpha AI V10.0 is Live on Render!")
        app.run_polling(drop_pending_updates=True)
