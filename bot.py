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
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- RENDER UPTIME SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Saeid Alpha AI is Running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- CONFIG & SECURITY ---
# Render-এর Environment Variables থেকে ডাটা নেবে
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "https://mn-chat-bot-api.vercel.app")
VERSION = "5.5.0 (Ultra Premium)"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ইন-মেমোরি ডাটাবেস
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- PREMIUM STYLING ---
HEADER = "✨ 𝐒𝐀𝐄𝐈𝐃 𝐀𝐋𝐏𝐇𝐀 𝐀𝐈 ✨\n"
LINE = "━━━━━━━━━━━━━━━━━━━━\n"
OWNER_LINK = "https://t.me/saeid_alpha_9"

# --- CORE FUNCTIONS ---

async def get_ai_response(user_id: int, user_name: str, user_text: str):
    """উন্নত বুদ্ধিমত্তা এবং মেমোরি কন্ট্রোল"""
    memory = user_memory[user_id][-10:] # ১০টি মেসেজ মনে রাখবে
    system_prompt = (
        f"You are Saeid Alpha AI, a sophisticated, helpful, and premium assistant. "
        f"The user's name is {user_name}. Provide expert-level answers."
    )
    
    payload = {
        "messages": [{"role": "system", "content": system_prompt}] + memory + [{"role": "user", "content": user_text}]
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/chat", json=payload, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "Internal Error.")
                return "❌ সার্ভার রেসপন্স দিচ্ছে না। কিছুক্ষণ পর চেষ্টা করুন।"
        except Exception:
            return "⚠️ কানেকশন এরর! আপনার নেটওয়ার্ক বা এপিআই চেক করুন।"

# --- COMMAND HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id]["requests"] += 1
    
    # প্রিমিয়াম ইনলাইন বাটন
    inline_kb = [
        [
            InlineKeyboardButton("📢 Developer", url=OWNER_LINK),
            InlineKeyboardButton("📊 Updates", url=OWNER_LINK)
        ],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    
    # রিপ্লাই কিবোর্ড (নিচের বাটন)
    reply_kb = [
        [KeyboardButton("🎨 AI Image"), KeyboardButton("🎭 Meme Maker")],
        [KeyboardButton("👤 My Profile"), KeyboardButton("🔥 Premium Features")]
    ]
    
    welcome_text = (
        f"{HEADER}{LINE}"
        f"স্বাগতম **{user.first_name}**! 👑\n\n"
        f"আমি আপনার ব্যক্তিগত আল্ট্রা-ইন্টেলিজেন্ট এআই সহকারী। "
        f"আমি কোডিং, ছবি তৈরি এবং যেকোনো জটিল প্রশ্নের সমাধান দিতে পারি।\n\n"
        f"🚀 **কিভাবে শুরু করবেন?**\n"
        f"• সরাসরি আমাকে কিছু জিজ্ঞেস করুন।\n"
        f"• নিচের বাটনগুলো ব্যবহার করে ফিচার এক্সপ্লোর করুন।"
    )
    
    await update.message.reply_text(
        welcome_text, 
        reply_markup=ReplyKeyboardMarkup(reply_kb, resize_keyboard=True),
        parse_mode=ParseMode.MARKDOWN
    )
    await update.message.reply_text("🔗 দ্রুত এক্সেস মেনু:", reply_markup=InlineKeyboardMarkup(inline_kb))

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stats = user_stats[user.id]
    profile_text = (
        f"{HEADER}{LINE}"
        f"👤 **Name:** {user.first_name}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"⚡ **Requests:** {stats['requests']}\n"
        f"📅 **Joined:** {stats['joined'].strftime('%d %b %Y')}\n"
        f"💎 **Status:** Verified Alpha User"
    )
    await update.message.reply_text(profile_text, parse_mode=ParseMode.MARKDOWN)

# --- MEDIA HANDLER ---

async def generate_media(update: Update, prompt: str, type: str):
    status = await update.message.reply_text(f"🚀 `{type}` প্রসেসিং হচ্ছে... একটু ধৈর্য ধরুন।")
    endpoint = "/image" if type == "Image" else "/meme"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}{endpoint}", json={"prompt": prompt}) as resp:
                data = await resp.json()
                img_url = data.get("image_url") or data.get("meme_url")
                
                if img_url:
                    await update.message.reply_photo(img_url, caption=f"✨ **{type} Generated!**\nPrompt: {prompt}", parse_mode=ParseMode.MARKDOWN)
                    await status.delete()
                else:
                    await status.edit_text("❌ এপিআই থেকে ছবি পাওয়া যায়নি।")
    except:
        await status.edit_text("⚠️ এরর! এপিআই সার্ভার ডাউন হতে পারে।")

# --- MESSAGE LOGIC ---

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_stats[user.id]["requests"] += 1

    # Route logic
    if text == "🎨 AI Image":
        return await update.message.reply_text("🖼 ছবি তৈরি করতে লিখুন: `/image [আপনার প্রম্পট]`")
    if text == "👤 My Profile":
        return await profile_handler(update, context)
    if text == "🎭 Meme Maker":
        return await update.message.reply_text("🎭 মিম তৈরি করতে লিখুন: `/meme [টেক্সট]`")
    if text == "🔥 Premium Features":
        return await update.message.reply_text("🌟 প্রিমিয়াম ফিচারে আপনাকে স্বাগতম! আপনি এখন আনলিমিটেড এআই পাওয়ার ব্যবহার করছেন।")

    # AI Chat Logic
    await update.message.chat.send_action(ChatAction.TYPING)
    response = await get_ai_response(user.id, user.first_name, text)
    
    # Save to memory
    user_memory[user.id].append({"role": "user", "content": text})
    user_memory[user.id].append({"role": "assistant", "content": response})
    
    await update.message.reply_text(f"👑 **Alpha AI:**\n\n{response}", parse_mode=ParseMode.MARKDOWN)

# --- MAIN RUNNER ---

def main():
    # Start Flask in background
    Thread(target=run_flask).start()

    # Build Bot
    app_bot = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("profile", profile_handler))
    app_bot.add_handler(CommandHandler("image", lambda u, c: generate_media(u, " ".join(c.args), "Image") if c.args else u.message.reply_text("প্রম্পট দিন!")))
    app_bot.add_handler(CommandHandler("meme", lambda u, c: generate_media(u, " ".join(c.args), "Meme") if c.args else u.message.reply_text("টেক্সট দিন!")))
    
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print(f"--- Saeid Alpha AI {VERSION} Started ---")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
