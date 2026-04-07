import logging
import requests
import re
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- কনফিগারেশন ---
TELEGRAM_TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API_URL = "https://mn-chat-bot-api.vercel.app/chat"
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
DEVELOPER_CHANNEL = "https://t.me/+0wBM6TCW4QxjNmI1"

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- এআই লজিক ---
SYSTEM_PROMPT = (
    "Your name is Saeid Alpha AI 👑. You are a highly professional, intelligent, and elite AI bot for Telegram. "
    "You were created by Saeid (@saeid9_90). You are an expert in all programming languages like Python, PHP, HTML, CSS, JS. "
    "When asked for code, always provide clean and optimized blocks. Keep your identity as 'Saeid Alpha AI 👑' consistently."
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
        return data.get('response') or data.get('content') or "I am analyzing the request... please wait."
    except:
        return "⚠️ Server busy. Please try again in a moment."

# --- কমান্ড ও বায়ো ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bio = (
        f"👑 **Saeid Alpha AI 👑 v3.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {user.first_name}\n"
        f"🤖 **Status:** Online & Ultra Intelligent\n"
        f"💻 **Expertise:** All Programming Languages\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🌟 **Professional Features:**\n"
        f"🚀 **Code Master:** Instantly write Python, PHP, or HTML.\n"
        f"🎨 **Photo Gen:** Use `/img [description]`\n"
        f"🧠 **Smart Brain:** Deep reasoning and problem solving.\n\n"
        f"⚡ **Let's start! How can I assist you today?**"
    )
    
    keyboard = [[InlineKeyboardButton("Developer Channel 👨‍💻", url=DEVELOPER_CHANNEL)]]
    await update.message.reply_text(bio, parse_mode=constants.ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

# --- ইমেজ জেনারেশন ---
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("❓ **Usage:** `/img futuristic landscape` ")
        return

    wait_msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is painting your imagination...")
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"{IMAGE_API_URL}{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
    
    try:
        await update.message.reply_chat_action(action=constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            photo=image_url, 
            caption=f"✅ **Art by Saeid Alpha AI 👑**\n📌 **Prompt:** {prompt}",
            parse_mode=constants.ParseMode.MARKDOWN
        )
        await wait_msg.delete()
    except:
        await wait_msg.edit_text("❌ Failed to generate image. Please try again.")

# --- মেসেজ হ্যান্ডলার ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    await update.message.reply_chat_action(action=constants.ChatAction.TYPING)
    response = get_ai_response(user_text)
    
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
    
    print("Saeid Alpha AI 👑 is Live!")
    application.run_polling()
    
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
