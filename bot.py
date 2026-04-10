import logging
import aiohttp
import asyncio
import os
from flask import Flask
from threading import Thread
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- FLASK SERVER ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Saeid Alpha AI is Running!", 200

def run():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
CHANNEL_LINK = "https://t.me/saeid_alpha_9"
VERSION = "5.2.0 (Chat ID Added)"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- KEYBOARDS ---
def main_menu_keyboard():
    kb = [
        [KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("👤 প্রোফাইল")],
        [KeyboardButton("💰 টাকা আয় করুন"), KeyboardButton("📜 সাহায্য")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# --- CORE FUNCTIONS ---
async def get_ai_response(user_id, user_name, user_text):
    context = user_memory[user_id][-5:]
    payload = {
        "messages": [{"role": "system", "content": f"You are Saeid Alpha AI. User: {user_name}."}] + context + [{"role": "user", "content": user_text}]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data.get("response", "Error!")
                    user_memory[user_id].append({"role": "user", "content": user_text})
                    user_memory[user_id].append({"role": "assistant", "content": reply})
                    return reply
        except: return "❌ কানেকশন এরর!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id # Chat ID সংগ্রহ
    
    welcome_text = (
        f"✨ <b>SAEID ALPHA AI</b> ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"স্বাগতম, <b>{user.first_name}</b>!\n"
        f"🆔 <b>Your Chat ID:</b> <code>{chat_id}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"চ্যাট করতে নিচে মেসেজ লিখুন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    text = update.message.text
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_stats[user.id]["requests"] += 1

    if text == "👤 প্রোফাইল":
        stats = user_stats[user.id]
        profile = (
            f"👤 <b>User Name:</b> {user.first_name}\n"
            f"🆔 <b>Chat ID:</b> <code>{chat_id}</code>\n" # প্রোফাইলে আইডি শো করবে
            f"📊 <b>Requests:</b> {stats['requests']}\n"
            f"📅 <b>Joined:</b> {stats['joined'].strftime('%d %b %Y')}"
        )
        return await update.message.reply_text(profile, parse_mode=ParseMode.HTML)

    # AI Chat Response with ID in footer
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    
    response_msg = (
        f"✨ <b>Saeid Alpha:</b>\n\n{reply}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>User:</b> {user.first_name} | 🆔 <b>ID:</b> <code>{chat_id}</code>"
    )
    await update.message.reply_text(response_msg, parse_mode=ParseMode.HTML)

# --- MAIN ---
def main():
    if not TELEGRAM_TOKEN: return
    keep_alive()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print(f"Bot Active with Chat ID support!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
