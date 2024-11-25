from sqlalchemy import delete, insert, select

from app.database import sessionmaker


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with sessionmaker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with sessionmaker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filters):
        async with sessionmaker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with sessionmaker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, **filter):
        async with sessionmaker() as session:
            stmt = delete(cls.model).filter_by(**filter)
            await session.execute(stmt)
            await session.commit()
