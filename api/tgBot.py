from telegram import Dispatcher, Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging

# Инициализируем бота
TELEGRAM_TOKEN = "7468098643:AAHhUFfJHb9DBsmpCRBwrYZFgTdHWuBYP1o"
bot = Bot(token=TELEGRAM_TOKEN)

# Инициализируем диспетчер для обработки событий
dispatcher = Dispatcher(bot, None, workers=0)

# Включаем логирование
logger = logging.getLogger(__name__)

# Обработчик команды /start
def start(update: Update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Привет! Я ваш бот!")

# Обработчик текстовых сообщений
def echo(update: Update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    context.bot.send_message(chat_id=chat_id, text=f"Вы сказали: {text}")

# Регистрация обработчиков
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Фоновая задача для обработки обновлений Telegram
async def process_update(update: dict):
    update_obj = Update.de_json(update, bot)
    dispatcher.process_update(update_obj)
