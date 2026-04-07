import logging
import requests
import re
import json
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- কনফিগারেশন ---
TELEGRAM_TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API_URL = "https://mn-chat-bot-api.vercel.app/chat"
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
DEVELOPER_CHANNEL = "https://t.me/+0wBM6TCW4QxjNmI1"

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- প্রিমিয়াম সিস্টেম প্রম্পট (বুদ্ধিমত্তা যোগ করা) ---
SYSTEM_INSTRUCTION = (
    "Your name is Saeid Alpha AI 👑. You are a highly intelligent, professional, and elite AI assistant "
    "specifically designed for Telegram. You are created by Saeid (@saeid9_90). "
    "You are an expert in all programming languages including Python, PHP, HTML, JavaScript, C++, and Java. "
    "When someone asks for code, provide clean, optimized, and well-commented code blocks. "
    "You are helpful, friendly, and you always maintain your identity as 'Saeid Alpha AI 👑'."
)

# --- AI চ্যাট ফাংশন ---
def get_ai_chat_response(user_text):
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        response = requests.post(CHAT_API_URL, json=payload, timeout=50)
        if response.status_code == 200:
            data = response.json()
            return data.get('response') or data.get('content') or "I am analyzing the data... please re-send."
        return "⚠️ Server is busy. Please try again in a moment."
    except Exception as e:
        return f"🛠 System Error: {str(e)}"

# --- স্টার্ট কমান্ড ও প্রিমিয়াম বায়ো ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    premium_bio = (
        f"✨ **Saeid Alpha AI 👑 v2.0** ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {user.first_name}\n"
        f"🤖 **Status:** Online & Ready\n"
        f"🛠 **Role:** Multi-Tasking AI Assistant\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔥 **Main Features:**\n"
        f"💻 **Expert Coding:** Python, PHP, HTML & more.\n"
        f"🖼 **AI Vision:** Use `/img` for High-End Art.\n"
        f"⚡ **Fast Execution:** No-lag AI Processing.\n\n"
        f"💡 **Command:** Try `/img cyber-city` or ask any code!"
    )
    
    keyboard = [
        [InlineKeyboardButton("Developer 👨‍💻", url=DEVELOPER_CHANNEL)],
        [InlineKeyboardButton("Official Channel 📢", url="https://t.me/saeid9_90")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        premium_bio, 
        parse_mode=constants.ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

# --- ইমেজ জেনারেশন ---
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("❓ **Usage:** `/img futuristic car` ")
        return

    wait_msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is rendering your imagination...")
    
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"{IMAGE_API_URL}{encoded_prompt}?width=1080&height=1080&model=flux&nologo=true"
    
    try:
        await update.message.reply_chat_action(action=constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            photo=image_url, 
            caption=f"✅ **Art by Saeid Alpha AI 👑**\n🎨 **Prompt:** {prompt}",
            parse_mode=constants.ParseMode.MARKDOWN
        )
        await wait_msg.delete()
    except:
        await wait_msg.edit_text("❌ Error generating image. Please try again.")

# --- স্মার্ট মেসেজ হ্যান্ডলার (Coding & Chat) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text: return

    await update.message.reply_chat_action(action=constants.ChatAction.TYPING)
    
    # কোডিং রিকোয়েস্ট কি না চেক করা (Simple Heuristic)
    coding_keywords = ['python', 'php', 'html', 'code', 'script', 'programming']
    
    response = get_ai_chat_response(user_text)
    
    # যদি কোড থাকে তবে Markdown এ পাঠানো
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- মেইন ফাংশন ---
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", generate_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Saeid Alpha AI 👑 is Online!")
    application.run_polling()
