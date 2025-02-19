import os
import g4f
from telethon import TelegramClient, events
import logging

# Уникальные идентификаторы для доступа к API Telegram.
# api_id и api_hash выдаются при регистрации приложения на https://my.telegram.org.
# Эти данные необходимы для авторизации и работы с Telegram API.

api_id = '' # Идентификатор приложения (Application ID)
api_hash = '' # Хэш приложения (Application Hash)
phone_number = 'YOUR_PHONE_NUMBER' 
session_name = 'session_name'
my_user_id =   # Здесь укажи свой User ID 
logging.basicConfig(level=logging.INFO)

if os.path.exists(f'{session_name}.session'):
    os.remove(f'{session_name}.session')
    logging.info("Старая сессия удалена.")

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage())
async def ai_response(event):
    if event.sender_id != my_user_id:
        return 

    user_message = event.message.text.strip()
    logging.info(f"Получено сообщение: {user_message}")

    if user_message.startswith("/"):
        question = user_message[1:].strip() 
        if not question:
            await event.reply("❌ Вы не задали вопрос после '/'. Пожалуйста, введите вопрос.")
            return
        
        try:
            logging.info(f"Отправляем запрос к GPT-4 с вопросом: {question}")
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}],
            )
            
            if isinstance(response, str):
                await event.reply(f"💭Ответ от ИИ: {response}") 
            elif isinstance(response, dict) and 'choices' in response:
                await event.reply(f"Ответ от ИИ: {response['choices'][0]['message']['content']}") 
            else:
                await event.reply("❌ Не удалось получить корректный ответ от модели.")
        except Exception as e:
            logging.error(f"Ошибка при запросе к GPT: {e}")
            await event.reply(f"⚠️ Произошла ошибка: {str(e)}")
    else:
        return

try:
    with client:
        client.start(phone_number)
        logging.info("Бот успешно запущен! Ожидание команд...")
        client.run_until_disconnected()
except Exception as e:
    logging.error(f"Ошибка при подключении: {e}")