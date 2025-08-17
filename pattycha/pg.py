from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Асинхронный движок (подставьте свою строку подключения)
DATABASE_URL = "postgresql+asyncpg://hackaton:sample-pass@127.0.0.1:5432/hackaton"

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логирования SQL

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей (если у вас уже есть MappedBase, оставьте его)
MappedBase = declarative_base()

# Генератор сессий для FastAPI/других асинхронных контекстов
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

from sqlalchemy import text

async def test_db_connection(user_id, book_id, page_id, text, answer):
    async with AsyncSessionLocal() as session:
        query = text("""
        INSERT INTO questions (
            user_id, 
            book_id, 
            page_id, 
            text, 
            answer, 
            period, 
            next_timestamp
        ) VALUES (
            :user_id, 
            :book_id, 
            :page_id, 
            :text, 
            :answer, 
            :period, 
            :next_timestamp
        )
        RETURNING id
    """)
    
    # Параметры для запроса
        params = {
            "user_id": user_id,
            "book_id": book_id,
            "page_id": page_id,
            "text": text,
            "answer": answer,
            "period": 0,
            "next_timestamp": datetime.now()
        }
        
        try:
            # Выполняем запрос
            result = await session.execute(query, params)
            await session.commit()
            
            # Получаем ID созданной записи
            created_id = result.scalar()
            return {
                "status": "success",
                "question_id": str(created_id),
            }
            
        except Exception as e:
            await session.rollback()
            return {
                "status": "error",
                "message": str(e)
            }


