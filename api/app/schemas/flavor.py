from pydantic import BaseModel
from typing import List, Optional

class FlavorBase(BaseModel):
    name: str

class FlavorCreate(FlavorBase):
    pass

class FlavorUpdate(FlavorBase):
    pass

class FlavorInDB(FlavorBase):
    id: int
    name: str

    class Config:
        orm_mode = True
