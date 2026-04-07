import logging, requests
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- Ultra Intelligence Coding Engine ---
async def get_ai_response(user_text):
    system_prompt = (
        "Your name is Saeid Alpha AI 👑. You are a Senior Software Engineer. "
        "You provide full code scripts in Python, PHP, HTML, CSS, JS, and more. "
        "Never say you cannot code. Always use markdown blocks for code. "
        "You are professional, elite, and created by Saeid (@saeid9_90)."
    )
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        r = requests.post(CHAT_API, json=payload, timeout=60)
        data = r.json()
        return data.get('response') or data.get('content') or "Analyzing code... please try again."
    except:
        return "⚠️ Brain connection lost. Try again in 5 seconds."

# --- Premium Dashboard Bio ---
async def start(update: Update, context: ContextTypes.import logging, requests, asyncio
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- High-Speed Coding Engine ---
async def get_ai_response(user_text):
    system_prompt = (
        "Your name is Saeid Alpha AI 👑. You are an expert Senior Developer. "
        "Provide full code in Python, PHP, HTML/CSS. Use clean Markdown blocks. "
        "Created by Saeid (@saeid9_90)."
    )
    payload = {"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}]}
    
    try:
        # টাইমিং সমস্যা দূর করতে timeout ৬০ সেকেন্ড করা হয়েছে
        r = await asyncio.to_thread(requests.post, CHAT_API, json=payload, timeout=60)
        data = r.json()
        return data.get('response') or data.get('content') or "I am processing the logic, please wait."
    except Exception as e:
        logging.error(f"Error: {e}")
        return "⚠️ Server is taking too long. Please try again in a moment."

# --- Premium Bio Interface ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    premium_ui = (
        f"👑 **Saeid Alpha AI v6.0 (Enterprise)** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Client:** {user.first_name}\n"
        f"🧠 **IQ Engine:** Ultra High (v6)\n"
        f"💻 **Expertise:** Advanced Coding & AI\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔥 **Main Features:**\n"
        f"✅ **Expert Coding:** Get Python, PHP, or HTML scripts.\n"
        f"✅ **Bug Fixer:** Debug your code instantly.\n"
        f"🎨 **Photo Art:** Generate art with `/img`.\n\n"
        f"💬 **How can Saeid Alpha help you today?**"
    )
    keyboard = [[InlineKeyboardButton("Join Developer Channel 👨‍💻", url=DEV_LINK)]]
    await update.message.reply_text(premium_ui, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# --- Image Generation ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("❓ **Usage:** `/img futuristic car` ")

    msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is rendering your art...")
    url = f"{IMG_API}{requests.utils.quote(prompt)}?width=1024&height=1024&model=flux&nologo=true"
    
    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(url, caption=f"✅ **By Saeid Alpha AI 👑**\n📌 {prompt}", parse_mode='Markdown')
        await msg.delete()
    except:
        await msg.edit_text("❌ Render failed.")

# --- Logic Chat Handler ---
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    
    response = await get_ai_response(update.message.text)
    
    # কোড সুন্দরভাবে দেখানোর জন্য সেফটি হ্যান্ডলিং
    if "```" in response:
        await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(response)

# --- App Runner ---
if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("img", img))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    print("Saeid Alpha AI v6.0 is Live!")
    application.run_polling()
):
    user = update.effective_user
    premium_bio = (
        f"🌌 **Saeid Alpha AI 👑 v5.0 (Global)**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Account:** {user.first_name}\n"
        f"🧠 **IQ Level:** 450+ (Super Intelligent)\n"
        f"💻 **Field:** Full-Stack & Cyber Security\n"
        f"🛰 **Status:** Online & Ready to Code\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💎 **Premium Features:**\n"
        f"🚀 **Code Generator:** Professional Python/PHP/HTML scripts.\n"
        f"🎨 **AI Image Art:** Generate art with `/img [prompt]`.\n"
        f"🛡 **Smart Logic:** Advanced reasoning for every query.\n\n"
        f"💬 **How can I assist you in your project today?**"
    )
    
    keyboard = [[InlineKeyboardButton("Developer Channel 👨‍💻", url=DEV_LINK)]]
    await update.message.reply_text(
        premium_bio, 
        parse_mode=constants.ParseMode.MARKDOWN, 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Professional Image Rendering ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("❓ **Usage:** `/img futuristic programming city` ")

    process = await update.message.reply_text("⏳ **Saeid Alpha AI** is rendering your vision...")
    encoded = requests.utils.quote(prompt)
    url = f"{IMG_API}{encoded}?width=1024&height=1024&model=flux&nologo=true"

    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(url, caption=f"🔥 **Premium Art by Saeid Alpha AI 👑**\n📌 {prompt}", parse_mode='Markdown')
        await process.delete()
    except:
        await process.edit_text("❌ Render failed. Try again.")

# --- Logic Message Handler ---
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text: return

    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    response = await get_ai_response(text)
    
    try:
        # কোড থাকলে তা সুন্দরভাবে দেখাবে
        if "```" in response:
            await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(response)
    except:
        await update.message.reply_text(response)

# --- Main App ---
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", img))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    
    print("Saeid Alpha AI 👑 v5.0 is Live!")
    app.run_polling()
