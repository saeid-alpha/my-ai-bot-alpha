import logging
import aiohttp
import asyncio
import os
from flask import Flask # à¦¨à¦¤à§à¦¨ à¦¯à§‹à¦— à¦•à¦°à¦¾ à¦¹à§Ÿà§‡à¦›à§‡
from threading import Thread # à¦¨à¦¤à§à¦¨ à¦¯à§‹à¦— à¦•à¦°à¦¾ à¦¹à§Ÿà§‡à¦›à§‡
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- FLASK SERVER FOR PORT ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Saeid Alpha AI is Running!"

def run():
    # Render à¦¡à¦¿à¦«à¦²à§à¦Ÿà¦­à¦¾à¦¬à§‡ à§§à§¦à§¦à§¦à§¦ à¦ªà§‹à¦°à§à¦Ÿ à¦¬à§à¦¯à¦¬à¦¹à¦¾à¦° à¦•à¦°à§‡
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIG & SECURITY ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
CHANNEL_LINK = "https://t.me/saeid_alpha_9"
AD_SITE_LINK = os.getenv("AD_SITE_LINK", "https://t.me/saeid_alpha_9")
VERSION = "5.0.0 (Web Port Enabled)"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Memory and Stats
user_memory = defaultdict(list)
user_stats = defaultdict(lambda: {"joined": datetime.now(), "requests": 0})

# --- STYLING & KEYBOARDS ---
HEADER = "âœ¨ <b>SAEID ALPHA AI | PREMIUM</b> âœ¨\n"
LINE = "<b>â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”</b>\n"

def main_menu_keyboard():
    kb = [[KeyboardButton("ðŸŽ¨ à¦à¦†à¦‡ à¦‡à¦®à§‡à¦œ"), KeyboardButton("ðŸŽ­ à¦®à§‡à¦® à¦®à§‡à¦•à¦¾à¦°")],
          [KeyboardButton("ðŸ’° à¦Ÿà¦¾à¦•à¦¾ à¦†à§Ÿ à¦•à¦°à§à¦¨"), KeyboardButton("ðŸ‘¤ à¦ªà§à¦°à§‹à¦«à¦¾à¦‡à¦²")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def income_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ”— à¦…à§à¦¯à¦¾à¦¡ à¦¦à§‡à¦–à§‡ à¦†à§Ÿ à¦•à¦°à§à¦¨", url=AD_SITE_LINK)],
                                 [InlineKeyboardButton("ðŸ“¢ à¦…à¦«à¦¿à¦¸à¦¿à§Ÿà¦¾à¦² à¦šà§à¦¯à¦¾à¦¨à§‡à¦²", url=CHANNEL_LINK)]])

# --- CORE FUNCTIONS ---
async def get_ai_response(user_id, user_name, user_text):
    payload = {"messages": [{"role": "system", "content": f"You are Saeid Alpha AI. User: {user_name}."}] + user_memory[user_id][-5:] + [{"role": "user", "content": user_text}]}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload, timeout=25) as resp:
                data = await resp.json()
                return data.get("response", "à¦¸à¦¾à¦°à§à¦­à¦¾à¦° à¦°à§‡à¦¸à¦ªà¦¨à§à¦¸ à¦¦à¦¿à¦šà§à¦›à§‡ à¦¨à¦¾à¥¤")
        except: return "âŒ à¦à¦ªà¦¿à¦†à¦‡ à¦•à¦¾à¦¨à§‡à¦•à¦¶à¦¨ à¦à¦°à¦°!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{HEADER}{LINE}à¦¸à§à¦¬à¦¾à¦—à¦¤à¦®! à¦†à¦®à¦¿ à¦à¦–à¦¨ à¦“à§Ÿà§‡à¦¬ à¦ªà§‹à¦°à§à¦Ÿà§‡ à¦²à¦¾à¦‡à¦­ à¦†à¦›à¦¿à¥¤", reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    if text == "ðŸ’° à¦Ÿà¦¾à¦•à¦¾ à¦†à§Ÿ à¦•à¦°à§à¦¨":
        return await update.message.reply_text("ðŸ’° à¦…à§à¦¯à¦¾à¦¡ à¦¦à§‡à¦–à§‡ à¦†à§Ÿ à¦•à¦°à¦¤à§‡ à¦¨à¦¿à¦šà§‡à¦° à¦¬à¦¾à¦Ÿà¦¨à§‡ à¦•à§à¦²à¦¿à¦• à¦•à¦°à§à¦¨à¥¤", reply_markup=income_keyboard(), parse_mode=ParseMode.HTML)
    
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await get_ai_response(user.id, user.first_name, text)
    await update.message.reply_text(f"âœ¨ <b>Saeid Alpha:</b>\n\n{reply}", parse_mode=ParseMode.HTML)

# --- MAIN ---
def main():
    if not TELEGRAM_TOKEN: return
    
    # à¦«à§à¦²à§à¦¯à¦¾à¦¸à§à¦• à¦¸à¦¾à¦°à§à¦­à¦¾à¦° à¦šà¦¾à¦²à§ à¦•à¦°à¦¾ à¦¹à¦šà§à¦›à§‡ (Port Bind à¦•à¦°à¦¾à¦° à¦œà¦¨à§à¦¯)
    keep_alive()
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print(f"Saeid Alpha AI {VERSION} is Live on Web Port!")
    app.run_polling()

if __name__ == "__main__":
    main()
