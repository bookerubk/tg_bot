from pydantic import BaseModel
from typing import Optional

# Модель для получения данных от вебхука Telegram
class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None
    edited_message: Optional[dict] = None
    channel_post: Optional[dict] = None
    edited_channel_post: Optional[dict] = None
