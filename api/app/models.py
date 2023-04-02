from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Strain(Base):
    __tablename__ = "strains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    strain_type = Column(String)
    feelings = Column(String)
    flavors = Column(String)
    helps_with = Column(String)
    thc_level = Column(String)
    dominant_terpene = Column(String)