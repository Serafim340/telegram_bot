import os
import json
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.helpers import escape_markdown
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("DEEPSEEK_API_KEY")
ALLOWED_USERS = set(map(int, os.getenv("ALLOWED_USERS", "").split(",")))

# Загружаем промт из внешнего файла
def load_prompt() -> str:
    try:
        with open("/etc/secrets/prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ Файл prompt.txt не найден. Пожалуйста, создайте его."

# Мини-сервер Flask для поддержки онлайн-состояния
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "✅ Бот работает!"

def run_web():
    app_web.run(host="0.0.0.0", port=8080)

# Разрешённые пользователи
def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# Запрос к DeepSeek API
def deepseek_search(prompt: str) -> str | None:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<your-username-or-site>",
                "X-Title": "<your-bot-name>",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {"role": "system", "content": load_prompt()},
                    {"role": "user", "content": prompt}
                ]
            })
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content")
    except Exception as e:
        print(f"API error: {e}")
        return None

# Команды Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_allowed(user.id):
        await update.message.reply_text("⛔ У вас нет доступа к этому боту.")
        return
    await update.message.reply_text("✅ Привет! Напиши, что хочешь создать ✨")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_allowed(user.id):
        await update.message.reply_text("⛔ У вас нет доступа к этому боту.")
        return

    prompt = update.message.text
    waiting = await update.message.reply_text("✍️ Думаю над твоим запросом...")
    result = deepseek_search(prompt)
    await waiting.delete()

    if result:
        cleaned = result.replace("*", "").replace("_", "").replace("~", "")
        escaped = escape_markdown(cleaned, version=2)
        await update.message.reply_text(escaped, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("❌ Не удалось получить ответ от нейросети.")

# Запуск
if __name__ == '__main__':
    if not TOKEN or not API_KEY:
        print("❌ Ошибка: отсутствуют переменные окружения.")
        exit(1)

    threading.Thread(target=run_web).start()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()
