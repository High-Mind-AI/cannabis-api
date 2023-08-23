from pydantic import BaseModel
from typing import Optional, List
from .feeling import FeelingInDB
from .flavor import FlavorInDB
from .helps_with import HelpsWithInDB
from .type import TypeInDB
from .terpene import TerpeneInDB


class StrainBase(BaseModel):
    name: str
    description: str
    thc_level: str


class StrainCreate(StrainBase):
    feelings: List[int] = []
    flavors: List[int] = []
    helps_with: List[int] = []
    strain_type_id: int
    dominant_terpene_id: Optional[int]


class StrainUpdate(StrainCreate):
    pass


class StrainInDB(StrainUpdate):
    id: int
    name: str
    description: str
    strain_type: TypeInDB
    feelings: List[FeelingInDB]
    flavors: List[FlavorInDB]
    helps_with: List[HelpsWithInDB]
    thc_level: str
    dominant_terpene: Optional[TerpeneInDB]

    class Config:
        orm_mode = True
