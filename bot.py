import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- সেটিংস ---
TELEGRAM_TOKEN = '8515258058:AAG-QCqbpo1UvjRahnW9oLnb5TGbp2GG34A'
API_URL = "https://mn-chat-bot-api.vercel.app/chat"

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- AI API থেকে উত্তর আনার ফাংশন ---
def get_ai_response(user_text):
    payload = {
        "messages": [{"role": "user", "content": user_text}]
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # আপনার API অনুযায়ী সঠিক কী (response) চেক করা হচ্ছে
            if 'response' in data:
                return data['response']
            
            # অন্যান্য সম্ভাব্য ফরম্যাট (সতর্কতা হিসেবে রাখা হলো)
            elif 'content' in data:
                return data['content']
            elif 'choices' in data:
                return data['choices'][0]['message']['content']
            else:
                return str(data) # যদি নতুন কিছু আসে তা দেখাবে
        else:
            return f"API Error: Status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- কমান্ড হ্যান্ডলার ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("বট এখন পুরোপুরি ঠিক আছে! কিছু লিখে পরীক্ষা করুন।")

# --- মেসেজ হ্যান্ডলার ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    if not user_msg:
        return

    await update.message.reply_chat_action(action="typing")
    ai_reply = get_ai_response(user_msg)
    await update.message.reply_text(ai_reply)

# --- মেইন রানার ---
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("বট সাকসেসফুলি আপডেট হয়েছে! এখন মেসেজ দিন।")
    application.run_polling()
