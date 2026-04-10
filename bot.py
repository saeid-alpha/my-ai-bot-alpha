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
        "Your name is Saeid Alpha AI ðŸ‘‘. You are a professional Senior Developer. "
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

    # à¦•à¦¾à¦¨à§‡à¦•à¦¶à¦¨ à¦à¦°à¦° à¦¹à§à¦¯à¦¾à¦¨à§à¦¡à§‡à¦² à¦•à¦°à¦¾à¦° à¦œà¦¨à§à¦¯ Retry Logic
    for attempt in range(3): 
        try:
            r = await asyncio.to_thread(requests.post, CHAT_API, json=payload, headers=headers, timeout=90)
            if r.status_code == 200:
                data = r.json()
                return data.get('response') or data.get('content') or "Analyzing... please wait."
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(2) # à§¨ à¦¸à§‡à¦•à§‡à¦¨à§à¦¡ à¦…à¦ªà§‡à¦•à§à¦·à¦¾ à¦•à¦°à§‡ à¦†à¦¬à¦¾à¦° à¦šà§‡à¦·à§à¦Ÿà¦¾ à¦•à¦°à¦¬à§‡
            
    return "âš ï¸ AI Server is busy. Please try asking again in a few seconds."

# --- Ultra Premium Bio ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    premium_ui = (
        f"ðŸ‘‘ **Saeid Alpha AI v7.0 (Stable)** ðŸ‘‘\n"
        f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        f"ðŸ‘¤ **Client:** {user.first_name}\n"
        f"ðŸ§  **Core:** Stable Intelligence v7\n"
        f"ðŸ’» **Field:** Coding & Logical Reasoning\n"
        f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
        f"ðŸ”¥ **Capabilities:**\n"
        f"âœ… **Code Generator:** Professional scripts for any project.\n"
        f"âœ… **Error Fixer:** Debug your code and find logic flaws.\n"
        f"ðŸŽ¨ **Image Creator:** Use `/img [prompt]` for art.\n\n"
        f"ðŸ’¬ **How can Saeid Alpha assist your coding today?**"
    )
    keyboard = [[InlineKeyboardButton("Support Developer ðŸ‘¨â€ðŸ’»", url=DEV_LINK)]]
    await update.message.reply_text(premium_ui, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# --- Professional Image Render ---
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        return await update.message.reply_text("â“ **Usage:** `/img futuristic programming setup` ")

    status_msg = await update.message.reply_text("â³ **Saeid Alpha AI** is rendering your vision...")
    url = f"{IMG_API}{requests.utils.quote(prompt)}?width=1024&height=1024&model=flux&nologo=true"
    
    try:
        await update.message.reply_chat_action(constants.ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(url, caption=f"âœ… **Art by Saeid Alpha AI ðŸ‘‘**\nðŸ“Œ {prompt}", parse_mode='Markdown')
        await status_msg.delete()
    except:
        await status_msg.edit_text("âŒ Render failed. Please try again.")

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
