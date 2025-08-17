from bot_tools.reg_user import register_user
from aiogram.types import Message

async def cmd_start(message: Message):
    user = message.from_user  # Объект пользователя
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# Отправляем запрос к API
    api_response = await register_user(user.id, user.first_name)
    
    if api_response:
        await message.answer("✅ Вы успешно зарегистрированы!\n"
                           f"Ответ сервера: {api_response}")
    else:
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")