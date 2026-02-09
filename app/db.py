from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from config import settings


DATABASE_URL = settings.get_database_url()

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    from models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_autos(autos_data: list):
    from models import Auto

    async with async_session() as session:
        async with session.begin():
            for auto_dict in autos_data:
                stmt = select(Auto).where(Auto.auto_id == auto_dict["auto_id"])
                result = await session.execute(stmt)
                existing_auto = result.scalar_one_or_none()

                if existing_auto:
                    for key, value in auto_dict.items():
                        setattr(existing_auto, key, value)
                else:
                    session.add(Auto(**auto_dict))
