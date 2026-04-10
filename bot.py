import logging
import aiohttp
import asyncio
import os
from datetime import datetime
from collections import defaultdict
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIG & SECURITY ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
VERSION = "4.1.0 (Ultra Premium Gold)"
PORT = int(os.environ.get("PORT", 10000)) # Render-এর জন্য পোর্ট

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FLASK SERVER FOR RENDER ---
app_flask = Flask(__name__)

@app_flask.route('/')
def health_check():
    return "Bot is Running!", 200

def run_flask():
    app_flask.run(host='0.0.0.0', port=PORT)

# --- MEMORY ---
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- STYLING ---
HEADER = "✨ <b>SAEID ALPHA AI | PREMIUM GOLD</b> ✨\n"
LINE = "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
FOOTER = "\n<i>Powered by Saeid Dev Team 👑</i>"

# --- CORE FUNCTIONS ---
async def get_ai_response(user_id: int, user_name: str, user_text: str):
    # মেমোরি ম্যানেজমেন্ট (সর্বশেষ ৮টি মেসেজ)
    memory = user_memory[user_id][-8:]
    system_prompt = f"You are Saeid Alpha AI 👑. User: {user_name}. Be creative and helpful."
    
    payload = {
        "messages": [{"role": "system", "content": system_prompt}] + memory + [{"role": "user", "content": user_text}]
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "সার্ভার থেকে সঠিক তথ্য পাওয়া যায়নি।")
                else:
                    return f"❌ API Error: Status {resp.status}"
        except asyncio.TimeoutError:
            return "⏳ রেসপন্স আসতে দেরি হচ্ছে, দয়া করে আবার চেষ্টা করুন।"
        except Exception as e:
            logger.error(f"AI Error: {e}")
            return "❌ এপিআই কানেকশন এরর বা ইন্টারনাল সমস্যা!"

# --- KEYBOARDS ---
def main_menu_keyboard():
    kb = [
        [KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("🎭 মেম মেকার")],
        [KeyboardButton("👤 প্রোফাইল"), KeyboardButton("📜 সাহায্য")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_stats[user.id]["requests"] += 1
        
        welcome_text = (
            f"{HEADER}{LINE}"
            f"স্বাগতম, <b>{user.first_name}</b>! 🌟\n\n"
            f"আমি আপনার পার্সোনাল এআই অ্যাসিস্ট্যান্ট। "
            f"নিচের মেনু ব্যবহার করে প্রিমিয়াম টুলসগুলো ট্রাই করুন।\n\n"
            f"💬 <b>চ্যাট করতে সরাসরি মেসেজ দিন!</b>\n"
            f"{LINE}{FOOTER}"
        )
        await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Start Error: {e}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user = update.effective_user
    user_stats[user.id]["requests"] += 1

    try:
        if text == "🎨 এআই ইমেজ":
            return await update.message.reply_text("🖼 <b>ইমেজ জেনারেটর:</b>\nলিখুন: <code>/image prompt</code>", parse_mode=ParseMode.HTML)
        
        if text == "👤 প্রোফাইল":
            stats = user_stats[user.id]
            profile_text = (f"👤 <b>Name:</b> {user.first_name}\n📊 <b>Queries:</b> {stats['requests']}\n🏆 <b>Status:</b> PREMIUM")
            return await update.message.reply_text(profile_text, parse_mode=ParseMode.HTML)

        # AI Chat
        await update.message.chat.send_action(ChatAction.TYPING)
        reply = await get_ai_response(user.id, user.first_name, text)
        
        # Save Memory
        user_memory[user.id].append({"role": "user", "content": text})
        user_memory[user.id].append({"role": "assistant", "content": reply})
        
        await update.message.reply_text(f"✨ <b>Saeid Alpha:</b>\n\n{reply}\n\n{LINE}", parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Text Handler Error: {e}")
        await update.message.reply_text("⚠️ দুঃখিত, কিছু একটা ভুল হয়েছে।")

# --- MAIN ---
def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN missing!")
        return

    # Flask রান করার জন্য আলাদা থ্রেড
    Thread(target=run_flask, daemon=True).start()

    # Bot Build
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print(f"--- Saeid Alpha AI {VERSION} is Active on Port {PORT} ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
