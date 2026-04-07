import logging
import requests
import re
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TELEGRAM_TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API_URL = "https://mn-chat-bot-api.vercel.app/chat"
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
DEVELOPER_CHANNEL = "https://t.me/+0wBM6TCW4QxjNmI1"

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Enhanced AI Logic ---
SYSTEM_PROMPT = (
    "Your name is Saeid Alpha AI 👑. You are a highly professional and intelligent AI bot operating on Telegram. "
    "You were created by Saeid (@saeid9_90). You are an expert in coding (Python, PHP, HTML, CSS, JS, etc.). "
    "Always provide code in clean markdown blocks. Be polite and helpful."
)

def get_ai_response(text):
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    }
    try:
        response = requests.post(CHAT_API_URL, json=payload, timeout=50)
        data = response.json()
        return data.get('response') or data.get('content') or "I am processing... please try again."
    except:
        return "⚠️ Server is busy. Please wait a moment."

# --- Start Command & Premium Bio ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bio = (
        f"👑 **Saeid Alpha AI v2.0** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {user.first_name}\n"
        f"🤖 **Identity:** Professional Telegram AI\n"
        f"💻 **Expertise:** All Programming Languages\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🌟 **Features:**\n"
        f"🚀 **Fast Code:** Ask any Python/PHP/HTML logic.\n"
        f"🎨 **AI Art:** Type `/img your_prompt`\n"
        f"🧠 **Smart Chat:** Advanced problem solving.\n\n"
        f"⚡ **Type anything to start chatting!**"
    )
    
    keyboard = [[InlineKeyboardButton("Developer Channel 👨‍💻", url=DEVELOPER_CHANNEL)]]
    await update.message.reply_text(bio, parse_mode=constants.ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

# --- Image Generation ---
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("⚠️ Please provide a description. Example: `/img a red sports car`")
        return

    await update.message.reply_chat_action(action=constants.ChatAction.UPLOAD_PHOTO)
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"{IMAGE_API_URL}{encoded_prompt}?width=1024&height=1024&model=flux"
    
    try:
        await update.message.reply_photo(photo=image_url, caption=f"✅ **Art by Saeid Alpha AI 👑**\n📌 **Prompt:** {prompt}", parse_mode=constants.ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error generating image. Try again later.")

# --- Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text: return

    await update.message.reply_chat_action(action=constants.ChatAction.TYPING)
    response = get_ai_response(user_text)
    
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- Main ---
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", generate_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Saeid Alpha AI 👑 is online!")
    application.run_polling()
        return
    
    response = get_ai_chat_response(user_text)
    
    # কোড ব্লক থাকলে সুন্দরভাবে ফরম্যাট করা
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- রানার ---
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", generate_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Saeid Alpha AI 👑 is now Deployed & Live!")
    application.run_polling()
            await update.message.reply_text("You haven't described what kind of image you want. Example: `/img dynamic Free Fire gaming logo with a lion mascot`")
            return
        await process_image_request(update, image_prompt)
        return
    
    response = get_ai_chat_response(user_text)
    
    # কোড ব্লক থাকলে সুন্দরভাবে ফরম্যাট করা
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- রানার ---
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", generate_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Saeid Alpha AI 👑 is now Deployed & Live!")
    application.run_polling()
