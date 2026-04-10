import os
from flask import Flask
from threading import Thread
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- রেন্ডারের জন্য ফ্লাস্ক সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha is Online! 👑"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- কিবোর্ড বাটন ---
def main_buttons():
    kb = [[KeyboardButton("🛠 টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI Mode"), KeyboardButton("🌦️ ওয়েদার")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# --- স্টার্ট কমান্ড ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 **Saeid Alpha AI V10.0**\n\nসাঈদ ভাই, আপনার সব টুলস নিচে দেওয়া হলো।",
        reply_markup=main_buttons()
    )

# --- মূল রানার ---
if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    if token:
        Thread(target=run).start()
        bot = Application.builder().token(token).build()
        bot.add_handler(CommandHandler("start", start))
        print("Bot is starting...")
        bot.run_polling(drop_pending_updates=True)
        
