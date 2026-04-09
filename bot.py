import logging
import aiohttp
import asyncio
import os
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIG & SECURITY ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
CHANNEL_LINK = "https://t.me/saeid_alpha_9"
AD_SITE_LINK = "https://your-income-site.com"  # এখানে আপনার ইনকাম সাইটের লিঙ্ক দিন
VERSION = "4.5.0 (Premium Income Edition)"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Memory and Stats
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- STYLING ---
HEADER = "✨ <b>SAEID ALPHA AI | PREMIUM</b> ✨\n"
LINE = "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"

# --- KEYBOARDS ---

def main_menu_keyboard():
    kb = [
        [KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("🎭 মেম মেকার")],
        [KeyboardButton("💰 টাকা আয় করুন"), KeyboardButton("👤 প্রোফাইল")],
        [KeyboardButton("📜 সাহায্য")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def income_keyboard():
    # এটি মেসেজের নিচে ইনলাইন বাটন হিসেবে দেখাবে
    keyboard = [
        [InlineKeyboardButton("🔗 অ্যাড দেখে আয় করুন", url=AD_SITE_LINK)],
        [InlineKeyboardButton("📢 অফিসিয়াল চ্যানেল", url=CHANNEL_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- CORE FUNCTIONS ---

async def get_ai_response(user_id, user_name, user_text):
    payload = {
        "messages": [{"role": "system", "content": f"You are Saeid Alpha AI. User: {user_name}."}] + user_memory[user_id][-5:] + [{"role": "user", "content": user_text}]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "সার্ভার রেসপন্স দিচ্ছে না।")
        except:
            return "❌ এপিআই কানেকশন এরর!"

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"{HEADER}{LINE}"
        f"স্বাগতম, <b>{user.first_name}</b>! 👑\n\n"
        f"আমি আপনার প্রিমিয়াম এআই অ্যাসিস্ট্যান্ট। "
        f"এখন আপনি আমার মাধ্যমে চ্যাট করার পাশাপাশি <b>টাকা আয়</b> করতে পারবেন!\n\n"
        f"👇 নিচের মেনু থেকে অপশন বেছে নিন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_stats[user.id]["requests"] += 1

    if text == "💰 টাকা আয় করুন":
        income_text = (
            f"💰 <b>আয় করার সুবর্ণ সুযোগ!</b>\n{LINE}"
            f"নিচের লিঙ্কে ক্লিক করে অ্যাড দেখুন এবং প্রতিদিন টাকা আয় করুন। "
            f"আপনার পেমেন্ট সরাসরি বিকাশ বা নগদে নিতে পারবেন।"
        )
        return await update.message.reply_text(income_text, reply_markup=income_keyboard(), parse_mode=ParseMode.HTML)

    if text == "👤 প্রোফাইল":
        stats = user_stats[user.id]
        profile_text = (
            f"👤 <b>ইউজার প্রোফাইল</b>\n{LINE}"
            f"নাম: {user.first_name}\n"
            f"স্ট্যাটাস: <b>PREMIUM GOLD</b>\n"
            f"মেম্বারশিপ: {stats['joined'].strftime('%d %b, %Y')}"
        )
        return await update.message.reply_text(profile_text, parse_mode=ParseMode.HTML, reply_markup=income_keyboard())

    if text == "🎨 এআই ইমেজ":
        return await update.message.reply_text("🖼 <b>ইমেজ জেনারেটর:</b>\nলিখুন: <code>/image আপনার প্রম্পট</code>", parse_mode=ParseMode.HTML)

    # General AI Chat
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    await update.message.reply_text(f"✨ <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN ---

def main():
    if not TELEGRAM_TOKEN: return
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print(f"Saeid Alpha AI {VERSION} is Live!")
    app.run_polling()

if __name__ == "__main__":
    main()
