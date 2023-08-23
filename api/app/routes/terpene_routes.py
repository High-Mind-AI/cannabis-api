from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..db import get_session
from ..models import Terpene  # This is the model name, so it should be singular
from ..schemas.terpene import TerpeneCreate, TerpeneUpdate, TerpeneInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# [Your terpene-related routes here]


# Get All Terpenes
@router.get("/terpenes", response_model=List[TerpeneInDB])
async def get_all_terpenes(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Terpene).order_by(Terpene.id)
        result = await s.execute(stmt)
        terpenes = result.scalars().all()
        return [TerpeneInDB(**f.__dict__) for f in terpenes]


# Terpene Create
@router.post("/terpene", response_model=TerpeneInDB)
async def create_terpene(
    terpene_create: TerpeneCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_terpene = Terpene(**terpene_create.dict())
        s.add(new_terpene)
        try:
            await s.commit()
            await s.refresh(new_terpene)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Terpene already exists")
    return TerpeneInDB(**new_terpene.__dict__)  # Convert ORM model to Pydantic


# Terpene Delete
@router.delete("/terpene/{terpene_id}", response_model=dict)
async def delete_terpene(
    type_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_terpene = await s.get(Terpene, type_id)
        if existing_terpene is None:
            raise HTTPException(status_code=404, detail="Terpene not found")
        await s.delete(existing_terpene)
        await s.commit()
        return {"Terpene deleted": existing_terpene.name}
