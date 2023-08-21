from pydantic import BaseModel
from typing import Optional, List
from .feeling import FeelingInDB
from .flavor import FlavorInDB


class StrainBase(BaseModel):
    name: str
    description: str
    strain_type: str
    helps_with: str
    thc_level: str
    dominant_terpene: str


class StrainCreate(StrainBase):
    feelings: List[int] = []
    flavors: List[int] = []


class StrainUpdate(StrainCreate):
    pass


class StrainInDB(StrainUpdate):
    id: int
    name: str
    description: str
    strain_type: str
    feelings: List[FeelingInDB]
    flavors: List[FlavorInDB]
    helps_with: str
    thc_level: str
    dominant_terpene: str

    class Config:
        orm_mode = True
