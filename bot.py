import os
import requests
from telegram.ext import Application, MessageHandler, filters

# جلب القيم من Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # مفتاح OpenRouter

# عنوان الـ API الخاص بـ OpenRouter
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def reply(update, context):
    user_message = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # أو gpt-4 أو أي موديل مجاني متاح عندك
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"⚠️ API Error: {e}"

    await update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("✅ Bot is running on Railway with OpenRouter...")
    app.run_polling()

if __name__ == "__main__":
    main()
