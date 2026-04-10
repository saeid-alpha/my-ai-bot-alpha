import logging
import requests
import sqlite3
from gtts import gTTS
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = "8505970978:AAGyclrkCZLPvSYDPcR7gfZ8rObNACIiZlk"
ADMIN_ID = 8247564821  # নিজের Telegram ID বসাও

# --- DB Setup ---
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, vip INTEGER)")
conn.commit()

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Memory ---
memory = {}

# --- Check VIP ---
def is_vip(user_id):
    cursor.execute("SELECT vip FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()
    return data and data[0] == 1

# --- AI Chat ---
def ai_chat(user_id, text):
    try:
        history = memory.get(user_id, "")
        prompt = history + "\nUser: " + text

        url = f"https://mn-chat-bot-api.vercel.app/chat?prompt={prompt}"
        res = requests.get(url)
        reply = res.text

        memory[user_id] = prompt + "\nAI: " + reply
        return reply
    except:
        return "⚠️ Error!"

# --- Voice ---
def text_to_voice(text):
    tts = gTTS(text)
    file = "voice.mp3"
    tts.save(file)
    return file

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 *Saeid Alpha AI*\n\n"
        "🔥 Ultra Premium Bot Ready!\n\n"
        "/ai text\n/code text\n/img text\n/voice text\n/vip\n/reset",
        parse_mode="Markdown"
    )

# --- VIP Info ---
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💎 VIP নিতে admin এর সাথে যোগাযোগ করুন")

# --- Admin Add VIP ---
async def addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    user_id = int(context.args[0])
    cursor.execute("INSERT INTO users VALUES (?, ?)", (user_id, 1))
    conn.commit()
    await update.message.reply_text("✅ User VIP Added")

# --- Reset Memory ---
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory.pop(update.message.from_user.id, None)
    await update.message.reply_text("🗑 Memory Cleared!")

# --- AI ---
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    reply = ai_chat(update.message.from_user.id, text)
    await update.message.reply_text(reply)

# --- Code ---
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    reply = ai_chat(update.message.from_user.id, "Write code: " + text)
    await update.message.reply_text("💻\n" + reply)

# --- Image (VIP only) ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_vip(user_id):
        await update.message.reply_text("🚫 VIP only feature")
        return

    text = " ".join(context.args)
    reply = ai_chat(user_id, "Create image prompt: " + text)
    await update.message.reply_text("🎨 " + reply)

# --- Voice ---
async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    file = text_to_voice(text)
    await update.message.reply_voice(voice=open(file, "rb"))

# --- Normal Chat ---
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ai_chat(update.message.from_user.id, update.message.text)
    await update.message.reply_text(reply)

# --- Main ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("addvip", addvip))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("ai", ai))
    app.add_handler(CommandHandler("code", code))
    app.add_handler(CommandHandler("img", img))
    app.add_handler(CommandHandler("voice", voice))

    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("🚀 Ultra Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
