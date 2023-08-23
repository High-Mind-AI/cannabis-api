from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Terpene(Base):
    __tablename__ = "terpenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    dominant_in_strains = relationship("Strain", back_populates="dominant_terpene")
    strains = relationship("Strain", secondary="strain_terpene", back_populates="terpenes")