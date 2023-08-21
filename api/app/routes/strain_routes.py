from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import subqueryload
from typing import List, Optional
from ..db import get_session
from ..models import Strain, Feeling, Flavor, HelpsWith
from ..schemas.strain import StrainCreate, StrainUpdate, StrainInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()

# ... all the strain-related routes ...


@router.get("/strains/{strain_name}", tags=["Strains"])
async def get_strain(strain_name: str, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = (
            select(Strain)
            .where(func.lower(Strain.name) == strain_name.lower())
            .options(subqueryload(Strain.feelings), subqueryload(Strain.flavors))
        )
        result = await s.execute(stmt)
        strain = result.scalar()
        if strain is None:
            raise HTTPException(
                status_code=404, detail=f"Strain {strain_name} not found"
            )
        return strain


@router.get("/strains", tags=["Strains"])
async def get_strains(count: int = 20, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = (
            select(Strain)
            .options(subqueryload(Strain.feelings), subqueryload(Strain.flavors))
            .order_by(Strain.id)
            .limit(count)
        )
        result = await s.execute(stmt)
        strains = result.scalars().all()
        return strains


@router.post("/strains", response_model=List[StrainInDB], tags=["Strains"])
async def create_strains(
    strains: List[StrainCreate],
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    created_strains = []

    async with session as s:
        # Begin a transaction
        await s.begin()

        for strain in strains:
            # Verify that all feelings exist
            feeling_objs = []
            for feeling_id in strain.feelings:
                stmt = select(Feeling).filter_by(id=feeling_id)
                result = await s.execute(stmt)
                feeling_obj = result.scalars().first()
                if not feeling_obj:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Feeling with ID {feeling_id} does not exist",
                    )
                feeling_objs.append(feeling_obj)

            # Verify that all flavors exist
            flavor_objs = []
            for flavor_id in strain.flavors:
                stmt = select(Flavor).filter_by(id=flavor_id)
                result = await s.execute(stmt)
                flavor_obj = result.scalars().first()
                if not flavor_obj:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Flavor with ID {flavor_id} does not exist",
                    )
                flavor_objs.append(flavor_obj)

            # Verify that all helps_with exist
            helps_with_objs = []
            for helps_with_id in strain.helps_with:
                stmt = select(HelpsWith).filter_by(id=helps_with_id)
                result = await s.execute(stmt)
                helps_with_obj = result.scalars().first()
                if not helps_with_obj:
                    raise HTTPException(
                        status_code=400,
                        detail=f"HelpsWith with ID {helps_with_id} does not exist",
                    )
                helps_with_objs.append(helps_with_obj)

            # Create the new strain without feelings and flavors
            new_strain = Strain(**strain.dict(exclude={"feelings", "flavors", "helps_with"}))

            # Set the feelings, flavors, helps_with
            new_strain.feelings = feeling_objs
            new_strain.flavors = flavor_objs
            new_strain.helps_with = helps_with_objs

            s.add(new_strain)
            await s.flush()  # Ensure new_strain gets an ID
            created_strains.append(new_strain)

        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Strain already exists")

    return created_strains


# Update an existing Strain
@router.put("/strains/{strain_id}", response_model=StrainInDB, tags=["Strains"])
async def update_strain(
    strain_id: int,
    strain: StrainUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_strain = await s.get(Strain, strain_id)
        if existing_strain is None:
            raise HTTPException(status_code=404, detail="Strain not found")
        for key, value in strain.dict(exclude_unset=True).items():
            setattr(existing_strain, key, value)
        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Strain already exists...")
        return existing_strain


# Delete an existing Strain
@router.delete("/strains/{strain_id}", response_model=dict, tags=["Strains"])
async def delete_strain(
    strain_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_strain = await s.get(Strain, strain_id)
        if existing_strain is None:
            raise HTTPException(status_code=404, detail="Strain not found")
        await s.delete(existing_strain)
        await s.commit()
        return {"Strain deleted": existing_strain.name}
