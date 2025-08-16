import uuid

from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4
    )
    
    username = Column(String, unique=True, index=True)
