import logging, requests, asyncio, time
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
CHAT_API = "https://mn-chat-bot-api.vercel.app/chat"
IMG_API = "https://image.pollinations.ai/prompt/"
DEV_LINK = "https://t.me/+0wBM6TCW4QxjNmI1"

logging.basicConfig(level=logging.INFO)

# --- Advanced Robust AI Engine ---
async def get_ai_response(user_text):
    system_prompt = (
        "Your name is Saeid Alpha AI 👑. You are a professional Senior Developer. "
        "Your goal is to write high-quality code in Python, PHP, HTML, CSS, and JS. "
        "Always provide complete scripts and use markdown code blocks. "
        "Created by Saeid (@saeid9_90)."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    # কানেকশন এরর হ্যান্ডেল করার জন্য Retry Logic
    for attempt in range(3): 
        try:
            r = await asyncio.to_thread(requests.post, CHAT_API, json=payload, headers=headers, timeout=90)
            if r.status_code == 200:
                data = r.json()
                return data.get('response') or data.get('content') or "Analyzing... please wait."
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(2) # ২ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে
            
    return "⚠️ AI Server is busy. Please try asking again in a few seconds."

# --- Ultra Premium Bio ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    premium_ui = (
        f"👑 **Saeid Alpha AI v7.0 (Stable)** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Client:** {user.first_name}\n"
        f"🧠 **Core:** Stable Intelligence v7\n"
        f"💻 **Field:** Coding & Logical Reasoning\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔥 **Capabilities:**\n"
        f"✅ **Code Generator:** Professional scripts for any project.\n"
        f"✅ **Error Fixer:** Debug your code and find logic flaws.\n"
        f"🎨 **Image Creator:** Use `/img [prompt]` for art.\n\n"
        f"💬 **How can Saeid Alpha assist your coding today?**"
    )
    keyboard = [[InlineKeyboardButton("Support Developer 👨‍💻", url=DEV_LINK)]]
    await update.message.reply_text(premium_ui, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# --- Professional Image Render ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("❓ **Usage:** `/img futuristic programming setup` ")

    status_msg = await update.message.reply_text("⏳ **Saeid Alpha AI** is rendering your vision...")
    url = f"{IMG_API}{requests.utils.quote(prompt)}?width=1024&height=1024&model=flux&nologo=true"
    
    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(url, caption=f"✅ **Art by Saeid Alpha AI 👑**\n📌 {prompt}", parse_mode='Markdown')
        await status_msg.delete()
    except:
        await status_msg.edit_text("❌ Render failed. Please try again.")

# --- Stable Chat Handler ---
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    await update.message.reply_chat_action(constants.ChatAction.TYPING)
    
    response = await get_ai_response(update.message.text)
    
    try:
        if "```" in response:
            await update.message.reply_text(response, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(response)
    except:
        await update.message.reply_text(response)

# --- Launcher ---
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", img))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    
    print("Saeid Alpha AI v7.0 is Online!")
    app.run_polling()
