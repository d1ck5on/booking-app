from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import JSON, NullPool
from typing import Annotated
from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL_asyncpg
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL_asyncpg
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    type_annotation_map = {
        dict: JSON
    }


intpk = Annotated[int, mapped_column(primary_key=True)]
