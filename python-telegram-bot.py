import asyncio
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- Твой токен ---
TOKEN = "8356139072:AAFhiu7mSCb431Ewa8-vnwIPVsLW9l46TyA"

# --- Логирование ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- Состояние игры ---
chat_id_global = None
messages = [
    "Лабубу голоден",
    "Лабубу грустно",
    "Лабубу скучно",
    "Лабубу хочет играть",
    "Лабубу устал",
    "Лабубу счастлив"
]

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id_global
    chat_id_global = update.effective_chat.id

    text = (
        "<b>Привет! 👋 Добро пожаловать в Labubu!</b>\n\n"
        "Ты попал в тёплый и весёлый мир Лабубу — виртуального питомца, которого можно кормить, развлекать и прокачивать.\n\n"
        "<b>Что можно делать:</b>\n"
        "• <b>Открывай сундуки</b> — внутри монеты, предметы и шанс выбить редкого питомца.\n"
        "• <b>Собирай и прокачивай</b> — корми, играй и открывай новые фишки.\n"
        "• <b>Приглашай друзей</b> — получай бонусы и сундуки.\n"
        "• <b>Зарабатывай награды</b> — выполняй задания и участвуй в ивентах.\n"
        "• <b>Стань самым крутым в школе</b> — собирай редкие скины и занимай лидерборд.\n\n"
        "Я буду присылать напоминания о Лабубу каждые 30 минут. Готов начать приключение?"
    )

    keyboard = [
        [InlineKeyboardButton("Играть ▶️", callback_data="play"),
         InlineKeyboardButton("Сундуки 🧰", callback_data="chests")],
        [InlineKeyboardButton("Пригласить друзей 🤝", callback_data="invite"),
         InlineKeyboardButton("Профиль 👤", callback_data="profile")],
        [InlineKeyboardButton("Помощь ❓", callback_data="help")]
    ]

    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

# --- Обработка нажатий на кнопки ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "play":
        await query.edit_message_text("🎮 Вы начали играть! Кормите Лабубу и открывайте сундуки.")
    elif data == "chests":
        await query.edit_message_text("🧰 Открывай сундуки каждый день, чтобы получить монеты и редких Лабубу!")
    elif data == "invite":
        await query.edit_message_text("🤝 Приглашайте друзей и получайте бонусы! Ссылка для приглашения: https://labubub-4mj5.vercel.app")
    elif data == "profile":
        await query.edit_message_text("👤 Здесь будет ваш профиль, уровень Лабубу и достижения.")
    elif data == "help":
        await query.edit_message_text("❓ Я буду присылать уведомления о Лабубу каждые 30 минут. Используйте кнопки для действий.")

# --- Фоновая задача для уведомлений ---
async def notifier(app: Application):
    global chat_id_global
    while True:
        if chat_id_global:
            text = random.choice(messages)
            await app.bot.send_message(chat_id=chat_id_global, text=text)
        await asyncio.sleep(1800)  # 30 минут

# --- Основная функция ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Фоновая задача
    async def background_task(context: ContextTypes.DEFAULT_TYPE):
        await notifier(app)

    # Запуск фоновой задачи при старте
    app.job_queue.run_once(lambda ctx: asyncio.create_task(background_task(ctx)), 1)

    app.run_polling()

if __name__ == "__main__":
    main()
