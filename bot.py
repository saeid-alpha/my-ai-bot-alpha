import logging, requests
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- কনফিগারেশন ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- এআই লজিক ---
async def get_reply(text):
    prompt = "Your name is Saeid Alpha AI 👑. You are a pro Telegram AI created by Saeid. You are expert in Python, PHP, HTML coding."
    payload = {"messages": [{"role": "system", "content": prompt}, {"role": "user", "content": text}]}
    try:
        r = requests.post(CHAT_API, json=payload, timeout=40)
        return r.json().get('response') or r.json().get('content') or "Try again."
    except: return "⚠️ Server busy."

# --- কমান্ডস ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bio = (f"👑 **Saeid Alpha AI 👑 v3.0**\n━━━━━━━━━━━━━━\n🤖 **Identity:** Telegram AI\n💻 **Expertise:** Code (Python, PHP, HTML)\n🎨 **Feature:** `/img prompt` to generate art.\n━━━━━━━━━━━━━━")
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("Developer Channel 👨‍💻", url=DEV_LINK)]])
    await update.message.reply_text(bio, parse_mode='Markdown', reply_markup=btn)

async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query: return await update.message.reply_text("Usage: `/img cat on a car`", parse_mode='Markdown')
    msg = await update.message.reply_text("⏳ Generating image...")
    url = f"{IMG_API}{requests.utils.quote(query)}?width=1024&height=1024&model=flux"
    try:
        await update.message.reply_photo(url, caption=f"✅ **By Saeid Alpha AI 👑**\n📌 {query}", parse_mode='Markdown')
        await msg.delete()
    except: await msg.edit_text("❌ Error.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    res = await get_reply(update.message.text)
    await update.message.reply_text(res, parse_mode='Markdown' if "```" in res else None)

# --- মেইন ---
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", img))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
