import logging, requests
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
# শক্তিশালী এপিআই যা কোডিং এ দক্ষ
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- Ultra Coding Engine ---
async def get_ai_response(user_text):
    # বটকে কোডিং এ দক্ষ করার ইনস্ট্রাকশন
    system_prompt = (
        "You are Saeid Alpha AI 👑, a Senior Full-Stack Developer. "
        "You are expert in Python, PHP, Java, HTML, CSS, JavaScript, and database management. "
        "Your task is to write high-quality, professional code for users. "
        "Always provide the full script and explain how to use it. "
        "Created by Saeid (@saeid9_90)."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    }
    
    try:
        # Timeout বাড়িয়ে দেয়া হয়েছে যাতে বড় কোড জেনারেট হতে পারে
        r = requests.post(CHAT_API, json=payload, timeout=60)
        data = r.json()
        return data.get('response') or data.get('content') or "I am processing your code... please try again."
    except:
        return "⚠️ Server is busy or API limit reached. Please try after 1 minute."

# --- Premium Interface ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bio = (
        f"👑 **Saeid Alpha AI v5.0 (Ultra)** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {user.first_name}\n"
        f"🚀 **Status:** Online & Ultra Intelligent\n"
        f"💻 **Role:** Senior Software Engineer\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔥 **Capabilities:**\n"
        f"✅ **Pro Coding:** Ask for any language script.\n"
        f"✅ **Advanced AI:** Solving logic & debugging.\n"
        f"✅ **Image Gen:** Create art with `/img`.\n\n"
        f"💬 **Send me any coding question or logic!**"
    )
    
    keyboard = [[InlineKeyboardButton("Developer & Channel 👨‍💻", url=DEV_LINK)]]
    await update.message.reply_text(bio, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# --- Image Generation ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("❓ **Usage:** `/img black hole wallpaper` ")

    msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is rendering your image...")
    url = f"{IMG_API}{requests.utils.quote(prompt)}?width=1024&height=1024&model=flux&nologo=true"

    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(url, caption=f"✅ **By Saeid Alpha AI 👑**\n📌 **Prompt:** {prompt}", parse_mode='Markdown')
        await msg.delete()
    except:
        await msg.edit_text("❌ Failed to generate image.")

# --- Optimized Message Handler ---
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text: return

    # টাইপিং অ্যাকশন দেখাবে যেন ইউজার বুঝতে পারে বট কাজ করছে
    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    
    response = await get_ai_response(text)
    
    # কোড সুন্দরভাবে দেখানোর জন্য Markdown ব্যবহার
    try:
        if "```" in response:
            await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(response)
    except:
        # যদি Markdown এ কোনো এরর হয় তবে সাধারণ টেক্সট পাঠাবে
        await update.message.reply_text(response)

# --- Start Bot ---
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", img))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    
    print("Saeid Alpha AI v5.0 is Running!")
    app.run_polling()
