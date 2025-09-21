import os
import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, Dispatcher

# Токен берём из переменной среды
TOKEN = os.environ["8356139072:AAFhiu7mSCb431Ewa8-vnwIPVsLW9l46TyA"]

# Состояние игры
messages = [
    "Лабубу голоден",
    "Лабубу грустно",
    "Лабубу скучно",
    "Лабубу хочет играть",
    "Лабубу устал",
    "Лабубу счастлив"
]

# Глобальный чат для уведомлений (в Webhook сложнее хранить, но для примера)
chat_ids = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_ids.add(chat_id)

    text = (
        "<b>Привет! 👋 Добро пожаловать в Labubu!</b>\n\n"
        "Ты попал в мир Лабубу — виртуального питомца!\n\n"
        "<b>Что делать:</b>\n"
        "• Открывай сундуки\n"
        "• Корми и играй с питомцем\n"
        "• Приглашай друзей\n"
        "• Получай награды\n"
    )

    keyboard = [
        [InlineKeyboardButton("Играть ▶️", callback_data="play")],
        [InlineKeyboardButton("Сундуки 🧰", callback_data="chests")],
        [InlineKeyboardButton("Пригласить друзей 🤝", callback_data="invite")],
    ]

    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "play":
        await query.edit_message_text("🎮 Вы начали играть!")
    elif data == "chests":
        await query.edit_message_text("🧰 Открывай сундуки!")
    elif data == "invite":
        await query.edit_message_text("🤝 Приглашайте друзей!")

# Создаём приложение
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(Dispatcher.callback_query_handler(button_handler))

# --- Главная функция для Vercel ---
async def handler(req, res):
    # req.json() — тело запроса от Telegram
    data = await req.json()
    update = Update.de_json(data, app.bot)
    await app.update_queue.put(update)
    await app.process_updates()
    return {"statusCode": 200, "body": "OK"}
