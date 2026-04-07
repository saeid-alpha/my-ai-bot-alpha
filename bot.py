import logging, requests
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration (Don't change spaces here) ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- Ultra Intelligence Engine ---
async def get_ai_response(user_text):
    # বটের মধ্যে অতিরিক্ত বুদ্ধিমত্তা এবং কোডিং দক্ষতা যোগ করার ইনস্ট্রাকশন
    intelligence_prompt = (
        "Your name is Saeid Alpha AI 👑. You are a Senior Software Engineer and AI Specialist. "
        "Created by Saeid (@saeid9_90), you are a professional Telegram assistant. "
        "You have expert knowledge in Python, PHP, HTML, CSS, JavaScript, and Server Management. "
        "When asked for code, always provide optimized, bug-free scripts in clean Markdown blocks. "
        "If a user wants to build a bot or website, give them step-by-step professional guidance."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": intelligence_prompt},
            {"role": "user", "content": user_text}
        ]
    }
    
    try:
        r = requests.post(CHAT_API, json=payload, timeout=50)
        data = r.json()
        return data.get('response') or data.get('content') or "I am currently analyzing the logic... please retry."
    except Exception:
        return "⚠️ Error connecting to AI brain. Please check your network."

# --- Premium Bio & Start Interface ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # একটি প্রিমিয়াম বায়ো এবং ইন্টারফেস ডিজাইন
    premium_ui = (
        f"🌌 **Saeid Alpha AI 👑 v4.0 (Enterprise)**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {user.first_name}\n"
        f"⚡ **System:** Online & Fully Intelligent\n"
        f"🛠 **Role:** Expert Full-Stack Developer\n"
        f"📡 **Server:** High-Performance Cloud\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💎 **Exclusive Capabilities:**\n"
        f"🚀 **Code Master:** Write/Debug Python, PHP & HTML.\n"
        f"🎨 **Vision Art:** Generate images using `/img` command.\n"
        f"🧠 **Deep Reasoning:** Solves complex logical problems.\n\n"
        f"💬 **How can Saeid Alpha assist you today?**"
    )
    
    keyboard = [[InlineKeyboardButton("Developer & Support 👨‍💻", url=DEV_LINK)]]
    await update.message.reply_text(
        premium_ui, 
        parse_mode=constants.ParseMode.MARKDOWN, 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Professional Image Render ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("❓ **Usage:** `/img futuristic cyberpunk lab` ")

    process_msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is creating your art...")
    encoded_query = requests.utils.quote(prompt)
    image_url = f"{IMG_API}{encoded_query}?width=1024&height=1024&model=flux&nologo=true"

    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            image_url, 
            caption=f"🔥 **Premium Art Generated**\n📌 **Request:** {prompt}", 
            parse_mode=constants.ParseMode.MARKDOWN
        )
        await process_msg.delete()
    except Exception:
        await process_msg.edit_text("❌ Failed to render image.")

# --- Smart Message Handler ---
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text: return

    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    response = await get_ai_response(text)
    
    # কোড ব্লক থাকলে সুন্দরভাবে ফরম্যাট করে পাঠানো
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- Run Application ---
if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", img))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    
    print("Saeid Alpha AI 👑 is now Live and Intelligent!")
    application.run_polling()
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
