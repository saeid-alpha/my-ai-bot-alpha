import os
import asyncio
import aiohttp
from flask import Flask
from threading import Thread
from datetime import datetime
from collections import defaultdict
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- FLASK SERVER (Render Fix) ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Saeid Alpha AI V10.0 is Live with All Tools! 👑", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
BANNER_URL = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"
ADMIN_ID = 6363842144

user_memory = defaultdict(list)
all_users = set()

# --- KEYBOARDS ---
def get_main_keyboard():
    kb = [
        [KeyboardButton("🛠 টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
        [KeyboardButton("🧠 AI Mode"), KeyboardButton("🌦️ ওয়েদার ও টাইম")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def get_toolbox_inline():
    buttons = [
        [InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data="t_img"),
         InlineKeyboardButton("🌐 অল ট্রান্সলেটর", callback_data="t_trans")],
        [InlineKeyboardButton("🎙 Text to Voice", callback_data="t_ttv"),
         InlineKeyboardButton("🎧 Voice to Text", callback_data="t_vtt")],
        [InlineKeyboardButton("💰 কারেন্সি", callback_data="t_curr"),
         InlineKeyboardButton("🔗 URL শর্টেনার", callback_data="t_url")],
        [InlineKeyboardButton("❌ মেনু বন্ধ", callback_data="close")]
    ]
    return InlineKeyboardMarkup(buttons)

# --- AI LOGIC ---
async def get_ai_response(user_id, user_name, text):
    system_prompt = f"You are Saeid Alpha AI 👑. User: {user_name}."
    history = user_memory[user_id][-5:]
    payload = {"messages": [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": text}]}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=20) as resp:
                data = await resp.json()
                reply = data.get("response", "সার্ভার ব্যস্ত।")
                user_memory[user_id].append({"role": "user", "content": text})
                user_memory[user_id].append({"role": "assistant", "content": reply})
                return reply
        except: return "❌ এপিআই কানেকশন এরর!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    msg = (f"👑 <b>Saeid Alpha AI V10.0</b>\n"
           f"━━━━━━━━━━━━━━━━━━━━━\n"
           f"স্বাগতম <b>{user.first_name}</b>!\n"
           f"আপনার সব প্রিমিয়াম টুলস এখন নিচের বাটনগুলোতে সাজানো আছে।")
    await update.message.reply_photo(BANNER_URL, caption=msg, reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "🛠 টুলবক্স":
        return await update.message.reply_text("💎 <b>সিলেক্ট করুন আপনার টুল:</b>", reply_markup=get_toolbox_inline(), parse_mode=ParseMode.HTML)

    if text == "👤 প্রোফাইল":
        return await update.message.reply_text(f"👤 <b>Profile:</b>\nID: <code>{user.id}</code>\nRank: <b>Elite</b>", parse_mode=ParseMode.HTML)

    if text == "🌦️ ওয়েদার ও টাইম":
        now = datetime.now().strftime("%I:%M %p | %d %b %Y")
        return await update.message.reply_text(f"⏰ <b>সময়:</b> {now}\n🌦️ শহর লিখে পাঠান ওয়েদার জানতে।", parse_mode=ParseMode.HTML)

    # AI Chat
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    await update.message.reply_text(f"👑 <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- BROADCAST ---
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return
    for u_id in all_users:
        try: await context.bot.send_message(u_id, f"📢 <b>ALERT:</b>\n\n{msg}", parse_mode=ParseMode.HTML)
        except: continue

# --- RUNNER ---
if __name__ == "__main__":
    if TELEGRAM_TOKEN:
        Thread(target=run_flask).start()
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("alert", alert))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        app.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer("শীঘ্রই চালু হচ্ছে!")))
        print("Saeid Alpha V10.0 is Running...")
        app.run_polling(drop_pending_updates=True)
                                    
