from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..db import get_session
from ..models import Feeling
from ..schemas.feeling import FeelingCreate, FeelingUpdate, FeelingInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# [Your feeling-related routes here]

# Get All Feelings
@router.get("/feelings", response_model=List[FeelingInDB], tags=["Feelings"])
async def get_all_feelings(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Feeling).order_by(Feeling.id)
        result = await s.execute(stmt)
        feelings = result.scalars().all()
        return [FeelingInDB(**f.__dict__) for f in feelings]


# Feelings Create
@router.post("/feelings", response_model=FeelingInDB, tags=["Feelings"])
async def create_feeling(
    feeling: FeelingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_feeling = Feeling(**feeling.dict())
        s.add(new_feeling)
        try:
            await s.commit()
            await s.refresh(new_feeling)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Feeling already exists")
    return FeelingInDB(**new_feeling.__dict__)  # Convert ORM model to Pydantic


# Feelings Delete
@router.delete("/feelings/{feeling_id}", response_model=dict, tags=["Feelings"])
async def delete_feeling(
    feeling_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_feeling = await s.get(Feeling, feeling_id)
        if existing_feeling is None:
            raise HTTPException(status_code=404, detail="Feeling not found")
        await s.delete(existing_feeling)
        await s.commit()
        return {"Feeling deleted": existing_feeling.name}