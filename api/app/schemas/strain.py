from pydantic import BaseModel
from typing import Optional, List
from .feeling import FeelingInDB
from .flavor import FlavorInDB
from .helps_with import HelpsWithInDB


class StrainBase(BaseModel):
    name: str
    description: str
    strain_type: str
    thc_level: str
    dominant_terpene: str


class StrainCreate(StrainBase):
    feelings: List[int] = []
    flavors: List[int] = []
    helps_with: List[int] = []


class StrainUpdate(StrainCreate):
    pass


class StrainInDB(StrainUpdate):
    id: int
    name: str
    description: str
    strain_type: str
    feelings: List[FeelingInDB]
    flavors: List[FlavorInDB]
    helps_with: List[HelpsWithInDB]
    thc_level: str
    dominant_terpene: str

    class Config:
        orm_mode = True
