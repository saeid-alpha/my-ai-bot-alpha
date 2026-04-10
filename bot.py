import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Render Port Binding ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha Pro is Live! 👑"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- Config ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 6363842144
all_users = set()

# --- Keyboards (Professional Layout) ---
def main_menu():
    kb = [[KeyboardButton("🛠 প্রিমিয়াম টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI চ্যাট"), KeyboardButton("📢 হেল্প ডেস্ক")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def tools_inline():
    btns = [[InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data='img'), InlineKeyboardButton("🎙 টেক্সট টু ভয়েস", callback_data='ttv')],
            [InlineKeyboardButton("🌐 অনুবাদক", callback_data='trans'), InlineKeyboardButton("💰 কারেন্সি", callback_data='curr')],
            [InlineKeyboardButton("🔗 URL শর্টেনার", callback_data='url'), InlineKeyboardButton("🎧 ভয়েস টু টেক্সট", callback_data='vtt')]]
    return InlineKeyboardMarkup(btns)

# --- Start Command (বাটন এখানে ফিক্স করা হয়েছে) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    
    welcome_msg = (f"👑 *Saeid Alpha AI V11.0*\n"
                   f"━━━━━━━━━━━━━━━━━━━━\n"
                   f"হ্যালো *{user.first_name}*!\n"
                   f"আপনার সব প্রফেশনাল টুলস এখন নিচের মেনুতে যুক্ত করা হয়েছে।")
    
    # ব্যক্তিগত চ্যাট ও গ্রুপ চেক
    if update.message.chat.type == 'private':
        await update.message.reply_text(welcome_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())
    else:
        await update.message.reply_text(f"👋 {user.first_name}, গ্রুপে স্বাগতম! আমাকে ইনবক্সে ব্যবহার করুন।")

# --- অল ইউজার অ্যালার্ট (Admin Only) ---
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return await update.message.reply_text("❌ ব্যবহার: `/alert আপনার মেসেজ`")
    
    count = 0
    for u_id in all_users:
        try:
            await context.bot.send_message(u_id, f"📢 *অফিসিয়াল ঘোষণা:*\n\n{msg}", parse_mode=ParseMode.MARKDOWN)
            count += 1
        except: continue
    await update.message.reply_text(f"✅ {count} জনের কাছে পাঠানো হয়েছে।")

# --- টেক্সট হ্যান্ডলার ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🛠 প্রিমিয়াম টুলবক্স":
        await update.message.reply_text("💎 *আপনার টুলবক্স:*", reply_markup=tools_inline(), parse_mode=ParseMode.MARKDOWN)
    elif text == "👤 প্রোফাইল":
        await update.message.reply_text(f"👤 *ইউজার প্রোফাইল:*\nনাম: {update.effective_user.first_name}\nস্ট্যাটাস: **Premium Gold** 👑", parse_mode=ParseMode.MARKDOWN)
    else:
        # সাধারণ চ্যাট রিপ্লাই
        await update.message.reply_text(f"👑 *Saeid Alpha:* আপনার মেসেজটি প্রসেস হচ্ছে...")

# --- রানার ---
if __name__ == "__main__":
    if TOKEN:
        Thread(target=run).start()
        bot = Application.builder().token(TOKEN).build()
        
        # কমান্ড হ্যান্ডলারগুলো সবার আগে থাকবে
        bot.add_handler(CommandHandler("start", start))
        bot.add_handler(CommandHandler("alert", alert))
        
        # টেক্সট মেসেজ হ্যান্ডলার
        bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Bot is starting...")
        bot.run_polling(drop_pending_updates=True)
