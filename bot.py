import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os
import httpx

async def register_user(tg_id: str, username: str):
    url = "https://prototype.bytecode.su/api/v1/user"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "tg_id": str(tg_id),
        "username": username
    }
    print(tg_id, type(tg_id), username, type(username))
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        
BOT_TOKEN = '8123025910:AAE1L4zJzNpovWe6JgzTSbNNHhU4fXyexJQ'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user  # Объект пользователя
    
# Отправляем запрос к API
    api_response = await register_user(user.id, user.first_name)
    
    if api_response:
        await message.answer("✅ Вы успешно зарегистрированы!\n"
                           f"Ответ сервера: {api_response}")
    else:
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")


# Обработчик всех текстовых сообщений
@dp.message()
async def echo_all(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())