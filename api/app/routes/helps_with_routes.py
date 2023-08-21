from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..db import get_session
from ..models import HelpsWith
from ..schemas.helps_with import HelpsWithCreate, HelpsWithUpdate, HelpsWithInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# [Your helps-with-related routes here]


# Get All HelpsWith
@router.get("/helpswith", response_model=List[HelpsWithInDB], tags=["HelpsWith"])
async def get_all_helps_with(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(HelpsWith).order_by(HelpsWith.id)
        result = await s.execute(stmt)
        helps_with = result.scalars().all()
        return [HelpsWithInDB(**f.__dict__) for f in helps_with]


# HelpsWith Create
@router.post("/helpswith", response_model=HelpsWithInDB, tags=["HelpsWith"])
async def create_helps_with(
    helps_with: HelpsWithCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_helps_with = HelpsWith(**helps_with.dict())
        s.add(new_helps_with)
        try:
            await s.commit()
            await s.refresh(new_helps_with)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="HelpsWith already exists")
    return HelpsWithInDB(**new_helps_with.__dict__)  # Convert ORM model to Pydantic


# HelpsWith Delete
@router.delete("/helpswith/{helps_with_id}", response_model=dict, tags=["HelpsWith"])
async def delete_helps_with(
    helps_with_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_helps_with = await s.get(HelpsWith, helps_with_id)
        if existing_helps_with is None:
            raise HTTPException(status_code=404, detail="HelpsWith not found")
        await s.delete(existing_helps_with)
        await s.commit()
        return {"HelpsWith deleted": existing_helps_with.name}
