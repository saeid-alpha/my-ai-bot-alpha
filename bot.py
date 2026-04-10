import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- Flask Server for Render ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha Premium is Online! 👑"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- Config ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 6363842144 # আপনার আইডি
BANNER = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"
all_users = set()

# --- Keyboards ---
def main_menu():
    kb = [[KeyboardButton("🛠 প্রিমিয়াম টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI চ্যাট"), KeyboardButton("📢 হেল্প ডেস্ক")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def tools_inline():
    btns = [[InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data='img'), InlineKeyboardButton("🎙 টেক্সট টু ভয়েস", callback_data='ttv')],
            [InlineKeyboardButton("🌐 অনুবাদক", callback_data='trans'), InlineKeyboardButton("💰 কারেন্সি", callback_data='curr')],
            [InlineKeyboardButton("🔗 URL শর্টেনার", callback_data='url'), InlineKeyboardButton("🎧 ভয়েস টু টেক্সট", callback_data='vtt')]]
    return InlineKeyboardMarkup(btns)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    
    # ব্যক্তিগত চ্যাটের ওয়েলকাম মেসেজ
    if update.message.chat.type == 'private':
        welcome = (f"👑 *Saeid Alpha AI V11.0*\n"
                   f"━━━━━━━━━━━━━━━━━━━━\n"
                   f"স্বাগতম *{user.first_name}*!\n\n"
                   f"আমি আপনার অল-ইন-ওয়ান এআই অ্যাসিস্ট্যান্ট। নিচের বাটন থেকে আপনার প্রয়োজনীয় টুলটি বেছে নিন।")
        await update.message.reply_photo(photo=BANNER, caption=welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())
    
    # গ্রুপে কেউ /start দিলে বা নতুন মেম্বার আসলে
    else:
        await update.message.reply_text(f"👋 হ্যালো {user.first_name}!\nগ্রুপে স্বাগতম। আমাকে ইনবক্সে ব্যবহার করতে @{context.bot.username} এ ক্লিক করুন।")

# --- গ্রুপে নতুন মেম্বার আসলে স্বাগতম বার্তা ---
async def welcome_group_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text("👑 Saeid Alpha AI এখন আপনার গ্রুপে! আমাকে অ্যাডমিন করে সব ফিচার উপভোগ করুন।")
        else:
            await update.message.reply_text(f"✨ স্বাগতম {member.first_name}!\nআমাদের গ্রুপে আপনাকে পেয়ে আমরা আনন্দিত। 😊")

# --- কাস্টম অ্যালার্ট (অ্যাডমিন শুধু ব্যবহার করতে পারবেন) ---
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg:
        return await update.message.reply_text("❌ ব্যবহার: `/alert আপনার মেসেজ`", parse_mode=ParseMode.MARKDOWN)
    
    count = 0
    for user_id in all_users:
        try:
            await context.bot.send_message(user_id, f"📢 *অফিসিয়াল ঘোষণা:*\n\n{msg}", parse_mode=ParseMode.MARKDOWN)
            count += 1
        except: continue
    await update.message.reply_text(f"✅ {count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🛠 প্রিমিয়াম টুলবক্স":
        await update.message.reply_text("💎 *আপনার টুলবক্স:*", reply_markup=tools_inline(), parse_mode=ParseMode.MARKDOWN)
    elif text == "👤 প্রোফাইল":
        await update.message.reply_text(f"👤 *ইউজার প্রোফাইল:*\nনাম: {update.effective_user.first_name}\nস্ট্যাটাস: **Premium Gold** 👑", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.chat.send_action(ChatAction.TYPING)
        await update.message.reply_text(f"👑 *Saeid Alpha:* আপনার মেসেজটি প্রসেস হচ্ছে...")

# --- Main Runner ---
if __name__ == "__main__":
    if TOKEN:
        Thread(target=run).start()
        app_bot = Application.builder().token(TOKEN).build()
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("alert", alert)) # /alert মেসেজ লিখে পাঠিয়ে দিন
        app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_group_member))
        app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        print("Saeid Alpha AI V11.0 is Live with Group & Alert features! 🚀")
        app_bot.run_polling(drop_pending_updates=True)
