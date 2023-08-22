from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..db import get_session
from ..models import Type  # This is the model name, so it should be singular
from ..schemas.type import TypeCreate, TypeUpdate, TypeInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# [Your type-related routes here]


# Get All Types
@router.get("/types", response_model=List[TypeInDB])
async def get_all_types(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Type).order_by(Type.id)
        result = await s.execute(stmt)
        types = result.scalars().all()
        return [TypeInDB(**f.__dict__) for f in types]


# Type Create
@router.post("/type", response_model=TypeInDB)
async def create_type(
    type_create: TypeCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_type = Type(**type_create.dict())
        s.add(new_type)
        try:
            await s.commit()
            await s.refresh(new_type)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Type already exists")
    return TypeInDB(**new_type.__dict__)  # Convert ORM model to Pydantic


# Type Delete
@router.delete("/type/{type_id}", response_model=dict)
async def delete_type(
    type_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_type = await s.get(Type, type_id)
        if existing_type is None:
            raise HTTPException(status_code=404, detail="Type not found")
        await s.delete(existing_type)
        await s.commit()
        return {"Type deleted": existing_type.name}
