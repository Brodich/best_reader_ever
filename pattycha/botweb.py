from dataclasses import dataclass
from configparser import ConfigParser
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from fastapi import FastAPI, Request, status
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from bot_tools.reg_user import register_user

@dataclass
class TelegramBot:
    filename: str = 'config.ini'
    
    def __post_init__(self) -> None:
        """Initialize bot client and configure logging."""
        self._setup_config()
        self._setup_logging()
        
        self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()
        self._register_handlers()
        
        self.app = FastAPI(
            title="Telegram Bot Webhook",
            lifespan=self.lifespan
        )
        self._setup_routes()
        
        self.logger.info("Bot initialized successfully")

    def _setup_config(self) -> None:
        """Read configuration from INI file."""
        self.cfg = ConfigParser()
        if not self.cfg.read(self.filename):
            raise FileNotFoundError(f"Config file {self.filename} not found")
        
        if not self.cfg.has_section('bot'):
            raise ValueError("Section 'bot' not found in config file")
        
        self.token = self.cfg.get('bot', 'token')
        self.webhook_path = self.cfg.get('bot', 'webhook_path', fallback='/webhook')
        self.webhook_url = self.cfg.get('bot', 'webhook')
        self.port = self.cfg.getint('bot', 'port', fallback=8000)
        self.log_file = self.cfg.get('bot', 'log_file', fallback='bot.log')

    def _setup_logging(self) -> None:
        """Configure logging system."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _register_handlers(self) -> None:
        """Register message handlers."""
        @self.dp.message(CommandStart())
        async def start_handler(message: Message):
            user = message.from_user  # Объект пользователя
            api_response = await register_user(str(user.id), user.first_name)
            print(user.id)
            if api_response:
                await message.answer("🚀 Пользователь зарегистрирован")
            else:
                await message.answer("🚀 Пользователь не зарегистрирован")
                

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        @self.app.post('/webhook')
        async def webhook_handler(request: Request):
            try:
                self.logger.info("Incoming webhook request")
                update_data = await request.json()
                update = Update.model_validate(update_data)
                await self.dp.feed_update(self.bot, update)
                return {"status": "ok"}
            except Exception as e:
                self.logger.error(f"Webhook error: {e}")
                return {"status": "error", "detail": str(e)}, status.HTTP_400_BAD_REQUEST

        @self.app.get("/send")
        async def send(id:int, text:str):
            await self.bot.send_message(chat_id=id, text=text)
            return {"status": "ok"}

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Async context manager for FastAPI lifespan."""
        self.logger.info("Setting up webhook...")
        await self.bot.set_webhook(
            url=f"{self.webhook_url}{self.webhook_path}",
            allowed_updates=self.dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        
        webhook_info = await self.bot.get_webhook_info()
        self.logger.info(f"Webhook info: {webhook_info}")
        
        yield
        
        self.logger.info("Deleting webhook...")
        await self.bot.delete_webhook()

    async def run(self):
        """Run the application."""
        self.logger.info(f"Starting server on port {self.port}")
        server = uvicorn.Server(
            config=uvicorn.Config(
                app=self.app,
                host="0.0.0.0",
                port=self.port,
                log_level="info"
            )
        )
        await server.serve()

async def main():
    bot = TelegramBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())