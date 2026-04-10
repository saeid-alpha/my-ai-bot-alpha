import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Render Setup ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha AI is Online! 👑"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- Config ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 6363842144
BANNER = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"
all_users = set()

# --- Professional Layout ---
def main_menu():
    kb = [[KeyboardButton("🛠 প্রিমিয়াম টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI চ্যাট"), KeyboardButton("📢 হেল্প ডেস্ক")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def tools_inline():
    btns = [[InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data='img'), InlineKeyboardButton("🎙 টেক্সট টু ভয়েস", callback_data='ttv')],
            [InlineKeyboardButton("🌐 অনুবাদক", callback_mode='trans'), InlineKeyboardButton("💰 কারেন্সি", callback_data='curr')],
            [InlineKeyboardButton("🔗 URL শর্টেনার", callback_data='url'), InlineKeyboardButton("🎧 ভয়েস টু টেক্সট", callback_data='vtt')]]
    return InlineKeyboardMarkup(btns)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    
    if update.message.chat.type == 'private':
        welcome = (f"👑 *স্বাগতম সাঈদ ভাই!*\n"
                   f"━━━━━━━━━━━━━━━━━━━━\n"
                   f"হ্যালো *{user.first_name}*! আমি আপনার সব ধরনের কোড, টেক্সট এবং জটিল প্রশ্নের উত্তর দিতে প্রস্তুত। 🚀")
        await update.message.reply_photo(photo=BANNER, caption=welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())
    else:
        await update.message.reply_text(f"👋 {user.first_name}, গ্রুপে স্বাগতম! আমাকে ব্যবহার করতে ইনবক্সে মেসেজ দিন।")

async def welcome_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"✨ স্বাগতম {member.first_name} আমাদের গ্রুপে! 😊")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return await update.message.reply_text("❌ ব্যবহার: `/alert আপনার ঘোষণা`")
    
    success = 0
    for u_id in all_users:
        try:
            await context.bot.send_message(u_id, f"📢 *অফিসিয়াল ঘোষণা:*\n\n{msg}", parse_mode=ParseMode.MARKDOWN)
            success += 1
        except: continue
    await update.message.reply_text(f"✅ {success} জন ইউজারের কাছে পাঠানো হয়েছে।")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🛠 প্রিমিয়াম টুলবক্স":
        await update.message.reply_text("💎 *আপনার টুলবক্স:*", reply_markup=tools_inline(), parse_mode=ParseMode.MARKDOWN)
    elif text == "👤 প্রোফাইল":
        await update.message.reply_text(f"👤 *প্রোফাইল:* {update.effective_user.first_name}\n🌟 *স্ট্যাটাস:* Premium Gold 👑")
    elif text == "🧠 AI চ্যাট":
        await update.message.reply_text("💬 *AI Mode:* আপনার কথা শোনার জন্য অপেক্ষা করছি! 🚀")
    else:
        await update.message.chat.send_action(ChatAction.TYPING)
        # এখানে আপনার Gemini বা অন্য AI API ইন্টিগ্রেশন হবে
        await update.message.reply_text(f"👑 *Saeid Alpha:* আপনার মেসেজটি প্রসেস হচ্ছে...")

# --- Run ---
if __name__ == "__main__":
    if TOKEN:
        Thread(target=run).start()
        bot = Application.builder().token(TOKEN).build()
        bot.add_handler(CommandHandler("start", start))
        bot.add_handler(CommandHandler("alert", alert))
        bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_group))
        bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        print("Saeid Alpha AI V12.0 is Live! 🚀")
        bot.run_polling(drop_pending_updates=True)
