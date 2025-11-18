from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from . import models


async def get_user_by_curp(db: AsyncSession, curp: str) -> Optional[models.Usuario]:
    result = await db.execute(
        select(models.Usuario).filter(models.Usuario.CURP == curp)
    )
    return result.scalars().first()


async def get_all_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[models.Usuario]:
    result = await db.execute(select(models.Usuario).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: dict) -> models.Usuario:
    db_user = models.Usuario(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    db: AsyncSession, curp: str, user_data: dict
) -> Optional[models.Usuario]:
    db_user = await get_user_by_curp(db, curp)
    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, curp: str) -> bool:
    db_user = await get_user_by_curp(db, curp)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


async def get_appointments_for_user(db: AsyncSession, curp: str) -> list[models.Citas]:
    result = await db.execute(
        select(models.Citas).filter(models.Citas.paciente_CURP == curp)
    )
    return result.scalars().all()