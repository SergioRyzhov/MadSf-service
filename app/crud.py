from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Meme
from .schemas import MemeCreate, MemeUpdate


async def get_meme(db: AsyncSession, meme_id: int):
    result = await db.execute(select(Meme).where(Meme.id == meme_id))
    return result.scalars().first()


async def get_memes(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Meme).offset(skip).limit(limit))
    return result.scalars().all()


async def create_meme(db: AsyncSession, meme: MemeCreate, image_url: str):
    db_meme = Meme(title=meme.title, description=meme.description, image_url=image_url)
    db.add(db_meme)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme


async def update_meme(db: AsyncSession, meme_id: int, meme: MemeUpdate):
    db_meme = await get_meme(db, meme_id)
    if db_meme is None:
        return None
    update_data = meme.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_meme, key, value)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme


async def delete_meme(db: AsyncSession, meme_id: int):
    db_meme = await get_meme(db, meme_id)
    if db_meme is None:
        return None
    await db.delete(db_meme)
    await db.commit()
    return db_meme
