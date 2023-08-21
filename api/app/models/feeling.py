from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Feeling(Base):
    __tablename__ = "feelings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # This relationship will give us feeling.strain_associations to access all associated strain-feeling records
    strain_associations = relationship("StrainFeeling", backref="feeling")
