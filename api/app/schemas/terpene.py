from pydantic import BaseModel
from typing import List, Optional

class TerpeneBase(BaseModel):
    name: str

class TerpeneCreate(TerpeneBase):
    pass

class TerpeneUpdate(TerpeneBase):
    pass

class TerpeneInDB(TerpeneBase):
    id: int
    name: str

    class Config:
        orm_mode = True
