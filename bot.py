import os
import logging
import aiohttp
import asyncio
from datetime import datetime
from collections import defaultdict
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- RENDER SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha AI is Online!"
def run_flask(): app.run(host='0.0.0.0', port=8080)

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "https://mn-chat-bot-api.vercel.app")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
user_memory = defaultdict(list)

# --- CORE AI LOGIC (With Retry) ---
async def get_ai_response(user_id, user_name, user_text):
    memory = user_memory[user_id][-10:]
    payload = {
        "messages": [
            {"role": "system", "content": f"You are Saeid Alpha AI, a pro assistant for {user_name}. Be very detailed."},
            *memory,
            {"role": "user", "content": user_text}
        ]
    }

    async with aiohttp.ClientSession() as session:
        for attempt in range(3):  # ৩ বার চেষ্টা করবে
            try:
                async with session.post(f"{API_URL}/chat", json=payload, timeout=70) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response")
            except:
                await asyncio.sleep(2) # ২ সেকেন্ড অপেক্ষা করে আবার ট্রাই করবে
        return "❌ এপিআই সার্ভার এখন খুব বিজি। দয়া করে ১ মিনিট পর আবার মেসেজ দিন।"

# --- WEATHER ---
async def get_weather(city):
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.wttr.in/{city}?format=%C+%t+%w"
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return f"🌡 **আবহাওয়া আপডেট: {city}**\n☁️ কন্ডিশন: {data}"
        except: pass
    return "⚠️ আবহাওয়া তথ্য পাওয়া যায়নি। শহরের নাম ঠিকভাবে লিখুন।"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("🎨 AI Image"), KeyboardButton("☁️ Weather")], [KeyboardButton("👤 Profile"), KeyboardButton("🛠 Support")]]
    await update.message.reply_text(
        f"✨ **SAEID ALPHA AI PRO** ✨\n━━━━━━━━━━━━━━━━━━━━\nস্বাগতম **{update.effective_user.first_name}**! 👑\nআমি এখন বড় বড় প্রশ্নের উত্তর দিতে প্রস্তুত।",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True), parse_mode=ParseMode.MARKDOWN
    )

async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🌟 **স্বাগতম {member.full_name}!**\nআমাদের গ্রুপে আপনাকে স্বাগতম। আমি আপনার এআই সহকারী।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text.lower().startswith("weather"):
        city = text.split(" ", 1)[1] if " " in text else "Dhaka"
        return await update.message.reply_text(await get_weather(city), parse_mode=ParseMode.MARKDOWN)

    if text == "☁️ Weather":
        return await update.message.reply_text("🌡 শহরের নামসহ লিখুন। যেমন: `weather Dhaka`")

    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    
    user_memory[user.id].append({"role": "user", "content": text})
    user_memory[user.id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(f"👑 **Alpha AI:**\n\n{reply}", parse_mode=ParseMode.MARKDOWN)

# --- RUN ---
def main():
    Thread(target=run_flask).start()
    app_bot = Application.builder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling(drop_pending_updates=True) # এটি Conflict Error কমাতে সাহায্য করবে

if __name__ == "__main__":
    main()
    
