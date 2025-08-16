from sqlalchemy.orm import DeclarativeBase, declared_attr


class MappedBase(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
