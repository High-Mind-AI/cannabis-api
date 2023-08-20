from pydantic import BaseModel
from typing import List, Optional

class FeelingBase(BaseModel):
    name: str

class FeelingCreate(FeelingBase):
    pass

class FeelingUpdate(FeelingBase):
    pass

class FeelingInDB(FeelingBase):
    id: int
    name: str

    class Config:
        orm_mode = True
