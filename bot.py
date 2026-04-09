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
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- FLASK SERVER (For Render Port Binding) ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Saeid Alpha AI V7.0 is Running on Web Port! 🚀"

def run_flask():
    # Render ডিফল্টভাবে এই পোর্টটি খোঁজে
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- CONFIG & STYLING ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
BANNER_URL = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg" # আপনার প্রচ্ছদ ছবির লিঙ্ক
HEADER = "💎 <b>SAEID ALPHA AI | V7.0 ULTRA</b> 💎\n"
LINE = "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"

# In-Memory Database (মেমোরি ও পরিসংখ্যান)
user_memory = defaultdict(list)
user_modes = {} 
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- KEYBOARDS ---
def main_menu():
    kb = [
        [KeyboardButton("🎨 ইমেজ তৈরি করুন"), KeyboardButton("💻 কোড জেনারেটর")],
        [KeyboardButton("🧠 AI Mode"), KeyboardButton("👤 মাই প্রোফাইল")],
        [KeyboardButton("📜 সাহায্য")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# --- CORE FUNCTIONS ---

async def get_ai_response(user_id, user_name, text):
    """শক্তিশালী বুদ্ধি সম্পন্ন AI রেসপন্স।"""
    mode = user_modes.get(user_id, "Smart")
    history = user_memory[user_id][-5:] # আগের ৫টি কথা মনে রাখবে
    
    # AI-কে তার পরিচয় এবং শক্তি সম্পর্কে ধারণা দেওয়া
    system_prompt = (
        f"Your name is Saeid Alpha AI 👑 (Saeid). You are a highly intellectual Telegram AI Bot. "
        f"User: {user_name}. Mode: {mode}. You can generate code, images, and answer complex questions. "
        f"Be helpful, professional, and remember you are the ultimate Saeid Alpha AI."
    )
    
    payload = {
        "messages": [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": text}]
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                data = await resp.json()
                reply = data.get("response", "সার্ভার রেসপন্স দিচ্ছে না।")
                
                # মেমোরি আপডেট
                user_memory[user_id].append({"role": "user", "content": text})
                user_memory[user_id].append({"role": "assistant", "content": reply})
                return reply
        except: return "❌ এপিআই কানেকশন এরর!"

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id]["requests"] += 1
    
    msg = (f"{HEADER}{LINE}"
           f"হ্যালো <b>{user.first_name}</b>!\n"
           f"আমি <b>Saeid Alpha AI 👑</b>। আমি এখন আগের চেয়ে বেশি শক্তিশালী।\n\n"
           f"✅ ইমেজ জেনারেশন\n✅ অ্যাডভান্সড কোডিং\n✅ চ্যাট মেমোরি\n\n"
           f"সবকিছু এখন আপনার হাতের মুঠোয়।")
    
    try:
        await update.message.reply_photo(BANNER_URL, caption=msg, reply_markup=main_menu(), parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text(msg, reply_markup=main_menu(), parse_mode=ParseMode.HTML)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stats = user_stats[user.id]
    profile_text = (
        f"👤 <b>ইউজার প্রোফাইল</b>\n{LINE}"
        f"নাম: {user.first_name}\n"
        f"🆔 <b>চ্যাট আইডি:</b> <code>{user.id}</code>\n"
        f"👤 <b>ইউজারনেম:</b> @{user.username if user.username else 'N/A'}\n"
        f"📊 <b>রিকোয়েস্ট:</b> {stats['requests']}\n"
        f"🏆 <b>স্ট্যাটাস:</b> PREMIUM GOLD\n{LINE}"
    )
    await update.message.reply_text(profile_text, parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_stats[user.id]["requests"] += 1

    if text == "🎨 ইমেজ তৈরি করুন":
        return await update.message.reply_text("🖼 ছবি তৈরি করতে লিখুন: <code>/image আপনার প্রম্পট</code>", parse_mode=ParseMode.HTML)
    
    if text == "👤 মাই প্রোফাইল":
        return await profile_handler(update, context)

    if text == "🧠 AI Mode":
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("😂 Funny", callback_data="mode_funny"), 
                                     InlineKeyboardButton("🧠 Smart", callback_data="mode_smart")],
                                    [InlineKeyboardButton("💻 Coding", callback_data="mode_coding")]])
        return await update.message.reply_text("🎭 <b>AI মোড সিলেক্ট করুন:</b>", reply_markup=btn, parse_mode=ParseMode.HTML)

    # Progress Bar ও AI চ্যাট
    status = await update.message.reply_text("<code>[▒▒▒▒▒▒▒▒▒▒] 10% Processing...</code>", parse_mode=ParseMode.HTML)
    reply = await get_ai_response(user.id, user.first_name, text)
    await status.delete()
    
    await update.message.reply_text(f"👑 <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- CALLBACK ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mode = query.data.split("_")[1].capitalize()
    user_modes[query.from_user.id] = mode
    await query.edit_message_text(f"✅ AI Mode: <b>{mode}</b>")

# --- MAIN RUNNER ---
if __name__ == "__main__":
    if TELEGRAM_TOKEN:
        # Flask Port Binding থ্রেড চালু করা
        Thread(target=run_flask).start()
        
        # বট অ্যাপ্লিকেশন
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("profile", profile_handler))
        app.add_handler(CallbackQueryHandler(button_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        print(f"Saeid Alpha AI V7.0 is Live on Port {os.environ.get('PORT', 10000)}")
        app.run_polling(drop_pending_updates=True)
