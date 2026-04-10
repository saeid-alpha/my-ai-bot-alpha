import logging
import aiohttp
import asyncio
import os
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- CONFIG & SECURITY ---
# টোকেন ও ইউআরএল রেন্ডার এনভায়রনমেন্ট থেকে আসবে
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
VERSION = "4.0.0 (Ultra Premium Gold)"

# Logging Configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Memory and Stats
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- PREMIUM STYLING ---
HEADER = "✨ <b>SAEID ALPHA AI | PREMIUM GOLD</b> ✨\n"
LINE = "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
FOOTER = "\n<i>Powered by Saeid Dev Team 👑</i>"

# --- CORE FUNCTIONS ---

async def get_ai_response(user_id: int, user_name: str, user_text: str):
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
                    return data.get("response", "সার্ভার রেসপন্স দিচ্ছে না।")
        except:
            return "❌ এপিআই কানেকশন এরর!"

# --- KEYBOARDS ---

def main_menu_keyboard():
    # এটি রিপ্লাই কিবোর্ড (নিচে স্থায়ী থাকবে)
    kb = [
        [KeyboardButton("🎨 এআই ইমেজ"), KeyboardButton("🎭 মেম মেকার")],
        [KeyboardButton("👤 প্রোফাইল"), KeyboardButton("📜 সাহায্য")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def inline_premium_links():
    # এটি মেসেজের সাথে বাটন হিসেবে থাকবে
    keyboard = [
        [InlineKeyboardButton("👑 Join Channel", url="https://t.me/Saeid_Alpha_AI"),
         InlineKeyboardButton("🛠 Support", url="https://t.me/Saeid_Alpha_AI")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    await update.message.reply_text(
        welcome_text, 
        reply_markup=main_menu_keyboard(), 
        parse_mode=ParseMode.HTML
    )

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stats = user_stats[user.id]
    profile_text = (
        f"🌟 <b>USER PREMIUM PROFILE</b> 🌟\n{LINE}"
        f"👤 <b>Name:</b> {user.first_name}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"📊 <b>Total Queries:</b> {stats['requests']}\n"
        f"📅 <b>Member Since:</b> {stats['joined'].strftime('%d %b, %Y')}\n"
        f"🏆 <b>Status:</b> <b>PREMIUM GOLD</b>\n{LINE}"
    )
    await update.message.reply_text(profile_text, parse_mode=ParseMode.HTML, reply_markup=inline_premium_links())

# --- HANDLERS ---

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_stats[user.id]["requests"] += 1

    if text == "🎨 এআই ইমেজ":
        return await update.message.reply_text("🖼 <b>ইমেজ জেনারেটর:</b>\nলিখুন: <code>/image আপনার প্রম্পট</code>", parse_mode=ParseMode.HTML)
    
    if text == "👤 প্রোফাইল":
        return await profile_handler(update, context)
    
    if text == "🎭 মেম মেকার":
        return await update.message.reply_text("🎭 <b>মিম জেনারেটর:</b>\nলিখুন: <code>/meme আপনার লেখা</code>", parse_mode=ParseMode.HTML)

    # General AI Chat
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    
    user_memory[user.id].append({"role": "user", "content": text})
    user_memory[user.id].append({"role": "assistant", "content": reply})
    
    formatted_reply = f"✨ <b>Saeid Alpha:</b>\n\n{reply}\n\n{LINE}"
    await update.message.reply_text(formatted_reply, parse_mode=ParseMode.HTML)

# --- MAIN ---

def main():
    if not TELEGRAM_TOKEN or not API_BASE_URL:
        print("Error: environment variables missing!")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile_handler))
    
    # Text Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print(f"--- Saeid Alpha AI {VERSION} is Active ---")
    app.run_polling()

if __name__ == "__main__":
    main()
