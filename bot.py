import os
import logging
import aiohttp
import asyncio
from datetime import datetime
from collections import defaultdict
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler

# --- RENDER UPTIME SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha AI is Online!"
def run_flask(): app.run(host='0.0.0.0', port=8080)

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "https://mn-chat-bot-api.vercel.app")
VERSION = "7.0.0 (Pro Master)"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_memory = defaultdict(list)

# --- UI CONSTANTS ---
HEADER = "✨ 𝐒𝐀𝐄𝐈𝐃 𝐀𝐋𝐏𝐇𝐀 𝐀𝐈 𝐏𝐑𝐎 ✨\n"
LINE = "━━━━━━━━━━━━━━━━━━━━\n"

# --- CORE FUNCTIONS ---

async def get_weather(city: str):
    """আবহাওয়া চেক করার ফাংশন"""
    # এখানে একটি পাবলিক এপিআই ব্যবহার করা হয়েছে
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.wttr.in/{city}?format=%C+%t+%w"
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return f"🌡 **আবহাওয়া আপডেট: {city}**\n☁️ কন্ডিশন: {data}"
                return "❌ শহরের নাম সঠিক নয় বা সার্ভার ডাউন।"
        except: return "⚠️ আবহাওয়া তথ্য পাওয়া যাচ্ছে না।"

async def get_ai_response(user_id: int, user_name: str, user_text: str):
    """বড় প্রশ্নের উত্তরের জন্য ইন্টেলিজেন্ট এআই"""
    memory = user_memory[user_id][-10:]
    system_prompt = (
        f"You are Saeid Alpha AI, a master developer and expert assistant. "
        f"User is {user_name}. Provide deep-dive answers for coding and long queries."
    )
    payload = {"messages": [{"role": "system", "content": system_prompt}] + memory + [{"role": "user", "content": user_text}]}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/chat", json=payload, timeout=60) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "No Response.")
                return "❌ সার্ভার বিজি। কিছুক্ষণ পর চেষ্টা করুন।"
        except: return "⚠️ রেসপন্স আসতে দেরি হচ্ছে। আবার ট্রাই করুন।"

# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = [
        [KeyboardButton("🎨 AI Image"), KeyboardButton("☁️ Weather")],
        [KeyboardButton("👤 Profile"), KeyboardButton("🛠 Support")]
    ]
    welcome = (
        f"{HEADER}{LINE}"
        f"স্বাগতম, **{user.first_name}**! 👑\n\n"
        f"আমি এখন যেকোনো বড় প্রশ্নের উত্তর এবং কোডিং সমাধান দিতে পারি।\n"
        f"গ্রুপে এড করলে আমি নতুন মেম্বারদের স্বাগতম জানাবো।\n\n"
        f"আবহাওয়া জানতে: `weather Dhaka` এভাবে লিখুন।"
    )
    await update.message.reply_text(welcome, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True), parse_mode=ParseMode.MARKDOWN)

# --- GROUP WELCOME FEATURE ---
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """গ্রুপে নতুন মেম্বার আসলে স্বাগতম জানাবে"""
    for member in update.message.new_chat_members:
        welcome_text = (
            f"🌟 **স্বাগতম {member.full_name}!**\n"
            f"আমাদের গ্রুপে আপনাকে স্বাগতম। আমি **Saeid Alpha AI**, "
            f"আপনার যেকোনো প্রয়োজনে আমি পাশে আছি। 😊"
        )
        await update.message.reply_text(welcome_text)

# --- HANDLERS ---

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    # Weather Logic
    if text.lower().startswith("weather"):
        city = text.split(" ", 1)[1] if " " in text else "Dhaka"
        result = await get_weather(city)
        return await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

    if text == "☁️ Weather":
        return await update.message.reply_text("🌡 আবহাওয়া জানতে শহরের নামসহ লিখুন। উদাহরণ: `weather Sylhet`")

    # AI Chat
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    
    user_memory[user.id].append({"role": "user", "content": text})
    user_memory[user.id].append({"role": "assistant", "content": reply})
    
    await update.message.reply_text(f"👑 **Alpha AI:**\n\n{reply}", parse_mode=ParseMode.MARKDOWN)

# --- RUN BOT ---
def main():
    Thread(target=run_flask).start()
    app_bot = Application.builder().token(TELEGRAM_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    # নতুন মেম্বার হ্যান্ডলার
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Saeid Alpha AI Pro Live...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
        
