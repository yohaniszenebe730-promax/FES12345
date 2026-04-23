import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# These will be set in the Render Dashboard for security
TOKEN = os.getenv("8377658343:AAFOuqkJTH1bKeyHmwyygmO_E71pGI1Q5Rk.")
HF_API_KEY = os.getenv("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")
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Welcome messages in 5 languages
WELCOME_TEXTS = {
    'en': "Welcome to FES AI! Ask me about Crypto, Technology, or Free Internet.",
    'am': "እንኳን ወደ FES AI በደህና መጡ! ስለ ክሪፕቶ፣ ቴክኖሎጂ ወይም ነፃ የኢንተርኔት አገልግሎት ይጠይቁኝ።",
    'om': "Baga nagaan gara FES AI dhuftan! Waa'ee Kiriyiptoo, Teknoolojii ykn tajaajila interneetii bilisaa na gaafadhaa.",
    'ti': "ናብ FES AI ብደሓን መጻእኩም! ብዛዕባ ክሪፕቶ፣ ቴክኖሎጂ ወይ ናጻ ኢንተርኔት ግልጋሎት ሕተቱኒ።",
    'ar': "مرحباً بكم في FES AI! اسألني عن الكريبتو، التكنولوجيا، أو خدمات الإنترنت المجانية."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'), 
         InlineKeyboardButton("Amharic 🇪🇹", callback_data='lang_am')],
        [InlineKeyboardButton("Afaan Oromoo", callback_data='lang_om'), 
         InlineKeyboardButton("Tigrinya", callback_data='lang_ti')],
        [InlineKeyboardButton("Arabic 🇸🇦", callback_data='lang_ar')],
        [InlineKeyboardButton("Join Community 📢", url="https://t.me/Free_Ethio_server_FES")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select Language / ቋንቋ ይምረጡ:", reply_markup=reply_markup)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]
    context.user_data['language'] = lang_code
    await query.edit_message_text(text=WELCOME_TEXTS[lang_code])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    # AI Processing
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": user_text})
    
    try:
        # Get AI response and append channel promotion
        bot_reply = response.json()[0]['generated_text']
        promo = "\n\n🚀 Join our channel for more: https://t.me/Free_Ethio_server_FES"
        await update.message.reply_text(f"{bot_reply}{promo}")
    except:
        await update.message.reply_text("Service is busy. Please try again or join @Free_Ethio_server_FES")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
