from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Feeling(Base):
    __tablename__ = "feelings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # This relationship will give us feeling.strain_associations to access all associated strain-feeling records
    strain_associations = relationship("StrainFeeling", backref="feeling")

class Strain(Base):
    __tablename__ = "strains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    strain_type = Column(String)
    
    # Directly point to Feeling using StrainFeeling as the association table
    feelings = relationship("Feeling", secondary="strain_feeling", backref="strains")

    flavors = Column(String)
    helps_with = Column(String)
    thc_level = Column(String)
    dominant_terpene = Column(String)

# Association table for Strain-Feeling relationship
class StrainFeeling(Base):
    __tablename__ = "strain_feeling"
    
    strain_id = Column(Integer, ForeignKey("strains.id"), primary_key=True)
    feeling_id = Column(Integer, ForeignKey("feelings.id"), primary_key=True)
    
    # Note: We don't need to explicitly define the backref relationships here, as we have already defined them using backref in the main models.
