from pydantic import BaseModel
from typing import Optional


class StrainBase(BaseModel):
    name: str
    description: str
    strain_type: str
    feelings: str
    flavors: str
    helps_with: str
    thc_level: str
    dominant_terpene: str


class StrainCreate(StrainBase):
    pass


class StrainUpdate(StrainCreate):
    pass


class StrainInDB(StrainUpdate):
    id: int
    name: str
    description: str
    strain_type: str
    feelings: str
    flavors: str
    helps_with: str
    thc_level: str
    dominant_terpene: str

    class Config:
        orm_mode = True
