from pydantic import BaseModel
from typing import List, Optional

class HelpsWithBase(BaseModel):
    name: str

class HelpsWithCreate(HelpsWithBase):
    pass

class HelpsWithUpdate(HelpsWithBase):
    pass

class HelpsWithInDB(HelpsWithBase):
    id: int
    name: str

    class Config:
        orm_mode = True
