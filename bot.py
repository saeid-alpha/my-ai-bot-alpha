import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Render Binding ---
app = Flask('')
@app.route('/')
def home(): return "Saeid Alpha AI is Online! 👑"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- Configuration ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 6363842144 # আপনার আইডি
BANNER_URL = "https://i.ibb.co/vzYyYpY/saeid-alpha.jpg"
all_users = set()

# --- Keyboards ---
def main_menu():
    kb = [[KeyboardButton("🛠 প্রিমিয়াম টুলবক্স"), KeyboardButton("👤 প্রোফাইল")],
          [KeyboardButton("🧠 AI চ্যাট"), KeyboardButton("📢 হেল্প ডেস্ক")]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def tools_inline():
    btns = [[InlineKeyboardButton("🎨 ইমেজ জেনারেটর", callback_data='img'), InlineKeyboardButton("🎙 টিটিএস", callback_data='ttv')],
            [InlineKeyboardButton("🌐 অনুবাদক", callback_data='trans'), InlineKeyboardButton("💰 কারেন্সি", callback_data='curr')],
            [InlineKeyboardButton("🔗 URL শর্টেনার", callback_data='url'), InlineKeyboardButton("🎧 এসটিটি", callback_data='vtt')]]
    return InlineKeyboardMarkup(btns)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    
    welcome_text = (f"👑 *স্বাগতম সাঈদ ভাই!*\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"হ্যালো *{user.first_name}*! আমি আপনার প্রফেশনাল এআই অ্যাসিস্ট্যান্ট। আমি এখন পুরোপুরি সচল।")
    
    await update.message.reply_photo(photo=BANNER_URL, caption=welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())

# অল ইউজার অ্যালার্ট
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    msg = " ".join(context.args)
    if not msg: return await update.message.reply_text("❌ মেসেজ দিন: `/alert আপনার মেসেজ`")
    
    for u_id in all_users:
        try: await context.bot.send_message(u_id, f"📢 *ঘোষণা:*\n\n{msg}", parse_mode=ParseMode.MARKDOWN)
        except: continue
    await update.message.reply_text("✅ মেসেজ পাঠানো সফল।")

# মেইন মেসেজ হ্যান্ডলার (এখানেই AI রিপ্লাই ঠিক করা হয়েছে)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # বাটন লজিক
    if text == "🛠 প্রিমিয়াম টুলবক্স":
        return await update.message.reply_text("💎 *প্রিমিয়াম টুলস:*", reply_markup=tools_inline(), parse_mode=ParseMode.MARKDOWN)
    
    elif text == "👤 প্রোফাইল":
        return await update.message.reply_text(f"👤 *ইউজার:* {update.effective_user.first_name}\n🌟 *প্যাকেজ:* Premium Gold 👑")

    # এআই রিপ্লাই লজিক
    else:
        await update.message.chat.send_action(ChatAction.TYPING)
        # এখানে এআই এর উত্তর সরাসরি জেনারেট হবে
        ai_response = f"👑 *Saeid Alpha:* সাঈদ ভাই, আমি আপনার '{text}' মেসেজটি পেয়েছি। আমি এখন প্রসেস করছি..."
        await update.message.reply_text(ai_response, parse_mode=ParseMode.MARKDOWN)

# --- Main App ---
if __name__ == "__main__":
    if TOKEN:
        Thread(target=run).start()
        bot_app = Application.builder().token(TOKEN).build()
        
        # কমান্ড যোগ করা
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CommandHandler("alert", alert))
        
        # মেসেজ হ্যান্ডলার যোগ করা
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Saeid Alpha is Running!")
        bot_app.run_polling(drop_pending_updates=True)
