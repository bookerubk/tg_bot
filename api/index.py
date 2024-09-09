from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import telegram

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен Telegram API
TELEGRAM_TOKEN = "7468098643:AAGKQOnW206tM59OwONqj0IDhSuEScrBGZo"
bot = Bot(token=TELEGRAM_TOKEN)

# Инициализируем FastAPI
app = FastAPI()

# Инициализируем диспетчер для обработки событий
dispatcher = Dispatcher(bot, None, workers=0)


# Модель для получения данных от вебхука Telegram
class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None
    edited_message: Optional[dict] = None
    channel_post: Optional[dict] = None
    edited_channel_post: Optional[dict] = None


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


# Маршрут для обработки вебхуков от Telegram
@app.post("/webhook")
async def telegram_webhook(update: TelegramWebhook, background_tasks: BackgroundTasks):
    # Передаем обновление в фоновую задачу для обработки
    background_tasks.add_task(process_update, update.dict())
    return {"status": "ok"}


# Маршрут для установки вебхука
@app.get("/set_webhook")
async def set_webhook():
    webhook_url = "https://tg-bot-git-main-bookerubks-projects.vercel.app/webhook"  # Укажите ваш URL для вебхука
    success = bot.set_webhook(webhook_url)
    if success:
        return {"message": "Webhook установлен"}
    else:
        return {"message": "Не удалось установить webhook"}


# Маршрут для удаления вебхука
@app.get("/delete_webhook")
async def del_webhook():
    success = bot.del_webhook()
    if success:
        return {"message": "Webhook удален"}
    else:
        return {"message": "Не удалось удалить webhook"}
