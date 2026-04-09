import logging
import aiohttp
import asyncio
import os
from flask import Flask # নতুন যোগ করা হয়েছে
from threading import Thread # নতুন যোগ করা হয়েছে
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- FLASK SERVER FOR PORT ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Saeid Alpha AI is Running!"

def run():
    # Render ডিফল্টভাবে ১০০০০ পোর্ট ব্যবহার করে
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIG & SECURITY ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
CHANNEL_LINK = "https://t.me/saeid_alpha_9"
AD_SITE_LINK = os.getenv("AD_SITE_LINK", "https://t.me/saeid_alpha_9")
VERSION = "5.0.0 (Web Port Enabled)"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Memory and Stats
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- STYLING & KEYBOARDS ---
HEADER = "✨ <b>SAEID ALPHA AI | PREMIUM</b> ✨\n"
LINE = "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"

def main_menu_keyboard():
    kb = [[KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("🎭 মেম মেকার")],
          [KeyboardButton("💰 টাকা আয় করুন"), KeyboardButton("👤 প্রোফাইল")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def income_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔗 অ্যাড দেখে আয় করুন", url=AD_SITE_LINK)],
                                 [InlineKeyboardButton("📢 অফিসিয়াল চ্যানেল", url=CHANNEL_LINK)]])

# --- CORE FUNCTIONS ---
async def get_ai_response(user_id, user_name, user_text):
    payload = {"messages": [{"role": "system", "content": f"You are Saeid Alpha AI. User: {user_name}."}] + user_memory[user_id][-5:] + [{"role": "user", "content": user_text}]}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                data = await resp.json()
                return data.get("response", "সার্ভার রেসপন্স দিচ্ছে না।")
        except: return "❌ এপিআই কানেকশন এরর!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{HEADER}{LINE}স্বাগতম! আমি এখন ওয়েব পোর্টে লাইভ আছি।", reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    if text == "💰 টাকা আয় করুন":
        return await update.message.reply_text("💰 অ্যাড দেখে আয় করতে নিচের বাটনে ক্লিক করুন।", reply_markup=income_keyboard(), parse_mode=ParseMode.HTML)
    
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    await update.message.reply_text(f"✨ <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN ---
def main():
    if not TELEGRAM_TOKEN: return
    
    # ফ্ল্যাস্ক সার্ভার চালু করা হচ্ছে (Port Bind করার জন্য)
    keep_alive()
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print(f"Saeid Alpha AI {VERSION} is Live on Web Port!")
    app.run_polling()

if __name__ == "__main__":
    main()
