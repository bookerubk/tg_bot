import json
import logging
from aiogram.types import Update
from config import Config
from handler import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handler(event, context):
    try:
        # 1. Логирование сырого запроса
        logger.info(f"Incoming event: {event}")
        
        # 2. Автоматическая обработка форматов
        body = event.get('body', event)
        if isinstance(body, str):
            body = json.loads(body)
        
        # 3. Создание гарантированно валидного Update
        update = Update.model_validate({
            'update_id': body.get('update_id', 1),
            'message': {
                'message_id': body.get('message', {}).get('message_id', 1),
                'from': {
                    'id': body.get('message', {}).get('from', {}).get('id', 1),
                    'is_bot': False,
                    'first_name': body.get('message', {}).get('from', {}).get('first_name', 'User')
                },
                'chat': body.get('message', {}).get('chat', {'id': 1, 'type': 'private'}),
                'date': body.get('message', {}).get('date', 1),
                'text': body.get('message', {}).get('text', '')
            }
        })
        
        # 4. Обработка через диспетчер
        await Config.dp.feed_update(bot=Config.bot, update=update)
        
        return {
            'statusCode': 200,
            'body': 'OK',
            'headers': {'Content-Type': 'text/plain'}
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal Error',
            'headers': {'Content-Type': 'text/plain'}
        }
