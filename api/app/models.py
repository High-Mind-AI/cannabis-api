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