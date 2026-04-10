import logging
import aiohttp
import asyncio
import os
from flask import Flask
from threading import Thread
from datetime import datetime
from collections import defaultdict
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- FLASK SERVER ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Saeid Alpha AI is Running! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
CHANNEL_LINK = "https://t.me/saeid_alpha_9"
AD_SITE_LINK = os.getenv("AD_SITE_LINK", "https://t.me/saeid_alpha_9")

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- AI LOGIC ---
async def get_ai_response(user_name, user_text):
    payload = {"messages": [{"role": "system", "content": f"You are Saeid Alpha AI. User: {user_name}."}, {"role": "user", "content": user_text}]}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                data = await resp.json()
                return data.get("response", "সার্ভার রেসপন্স দিচ্ছে না।")
        except: return "❌ এপিআই কানেকশন এরর!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("💰 টাকা আয় করুন")]]
    await update.message.reply_text("✨ <b>স্বাগতম!</b> আমি এখন লাইভ আছি।", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "💰 টাকা আয় করুন":
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 অ্যাড দেখুন", url=AD_SITE_LINK)]])
        return await update.message.reply_text("💰 আয় করতে নিচের বাটনে ক্লিক করুন।", reply_markup=btn, parse_mode=ParseMode.HTML)
    
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(update.effective_user.first_name, text)
    await update.message.reply_text(f"👑 <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN RUNNER ---
if __name__ == "__main__":
    if TELEGRAM_TOKEN:
        # Flask কে আলাদা থ্রেডে চালানো
        Thread(target=run_flask).start()
        
        # টেলিগ্রাম বট রান করা
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        print("Bot is Polling...")
        app.run_polling(drop_pending_updates=True)
