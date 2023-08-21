from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..db import get_session
from ..models import Flavor
from ..schemas.flavor import FlavorCreate, FlavorUpdate, FlavorInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# [Your flavor-related routes here]


# Get All Flavors
@router.get("/flavors", response_model=List[FlavorInDB], tags=["Flavors"])
async def get_all_flavors(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Flavor).order_by(Flavor.id)
        result = await s.execute(stmt)
        flavors = result.scalars().all()
        return [FlavorInDB(**f.__dict__) for f in flavors]


# Flavors Create
@router.post("/flavors", response_model=FlavorInDB, tags=["Flavors"])
async def create_flavor(
    flavor: FlavorCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_flavor = Flavor(**flavor.dict())
        s.add(new_flavor)
        try:
            await s.commit()
            await s.refresh(new_flavor)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Flavor already exists")
    return FlavorInDB(**new_flavor.__dict__)  # Convert ORM model to Pydantic


# Flavors Delete
@router.delete("/flavors/{flavor_id}", response_model=dict, tags=["Flavors"])
async def delete_flavor(
    flavor_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_flavor = await s.get(Flavor, flavor_id)
        if existing_flavor is None:
            raise HTTPException(status_code=404, detail="Flavor not found")
        await s.delete(existing_flavor)
        await s.commit()
        return {"Flavor deleted": existing_flavor.name}
