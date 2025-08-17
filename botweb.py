import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn
from contextlib import asynccontextmanager

bot = Bot(token='8123025910:AAE1L4zJzNpovWe6JgzTSbNNHhU4fXyexJQ',
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url="test.bytecode.su/webhook",
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


@dp.message(CommandStart())
async def start(message: Message) -> None:

    await message.answer('Привет!')


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8001)