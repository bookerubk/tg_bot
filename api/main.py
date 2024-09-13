from fastapi import FastAPI, BackgroundTasks
from tgBot import process_update, bot
from models import TelegramWebhook

# Инициализируем FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}
    
# Маршрут для обработки вебхуков от Telegram
@app.post("/webhook")
async def telegram_webhook(update: TelegramWebhook, background_tasks: BackgroundTasks):
    # Передаем обновление в фоновую задачу для обработки
    background_tasks.add_task(process_update, update.dict())
    return {"status": "ok"}

# Маршрут для установки вебхука
@app.get("/set_webhook")
async def set_webhook():
    webhook_url = "https://tg-icvi1da20-bookerubks-projects.vercel.app/webhook"  # Укажите ваш URL для вебхука
    success = bot.set_webhook(webhook_url)
    if success:
        return {"message": "Webhook установлен"}
    else:
        return {"message": "Не удалось установить webhook"}

# Маршрут для удаления вебхука
@app.get("/delete_webhook")
async def del_webhook():
    success = bot.delete_webhook()
    if success:
        return {"message": "Webhook удален"}
    else:
        return {"message": "Не удалось удалить webhook"}
