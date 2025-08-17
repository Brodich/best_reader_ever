from dataclasses import dataclass
from configparser import ConfigParser
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn
from contextlib import asynccontextmanager
from  bot_tools.func import *

@dataclass
class bot:
    filename: str = 'config.ini'
    
    def __post_init__(self) -> None:
        """Initialize text_processor client and configure logging."""
        self._setup_config()
        self._setup_logging()
        
        self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()
        
        self.app = FastAPI(lifespan=self.lifespan)
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)
        self.logger.info("bot initialized")

    def _setup_config(self) -> None:
        """Read configuration from INI file."""
        self.cfg = ConfigParser()
        self.cfg.read(self.filename)
        
        self.webhook = self.cfg.get('bot', 'webhook')
        self.token = self.cfg.get('bot', 'token')
        self.port = int(self.cfg.get('bot', 'port'))
        self.log_file = self.cfg.get('bot', 'log_file')

    def _setup_logging(self) -> None:
        """Configure logging system."""
        self.logger  = logging.getLogger(self.log_file)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(file_handler)

    
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self.bot.set_webhook(url="test.bytecode.su/webhook",
                            allowed_updates=self.dp.resolve_used_update_types(),
                            drop_pending_updates=True)
        yield
        await self.bot.delete_webhook()

    async def _setup_webhook_handler(self):
        """Добавляем обработчик вебхука для FastAPI"""
        @self.app.post("/webhook")
        async def webhook_handler(request: Request):
            try:
                update = Update(**await request.json())
                await self.dp.feed_update(self.bot, update)
                return {"status": "ok"}
            except Exception as e:
                self.logger.error(f"Webhook error: {e}")
                return {"status": "error", "detail": str(e)}

a = bot()
cmd_start = a.dp.message(Command("start"))(cmd_start)