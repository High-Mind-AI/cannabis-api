from pydantic import BaseModel
from typing import List, Optional

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class TypeUpdate(TypeBase):
    pass

class TypeInDB(TypeBase):
    id: int
    name: str

    class Config:
        orm_mode = True
