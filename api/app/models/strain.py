from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Strain(Base):
    __tablename__ = "strains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    # Directly point to Type (the strain's type, e.g., Indica, Hybrid, Sativa)
    strain_type_id = Column(Integer, ForeignKey("types.id"))
    strain_type = relationship("Type")

    # Directly point to Feeling using StrainFeeling as the association table
    feelings = relationship("Feeling", secondary="strain_feeling", backref="strains")

    # Directly point to Flavor using StrainFlavor as the association table
    flavors = relationship("Flavor", secondary="strain_flavor", backref="strains")

    # Directly point to HelpsWith using StrainHelpsWith as the association table
    helps_with = relationship(
        "HelpsWith", secondary="strain_helps_with", backref="strains"
    )

    thc_level = Column(String)
    dominant_terpene = Column(String)


# Association table for Strain-Feeling relationship
class StrainFeeling(Base):
    __tablename__ = "strain_feeling"

    strain_id = Column(Integer, ForeignKey("strains.id"), primary_key=True)
    feeling_id = Column(Integer, ForeignKey("feelings.id"), primary_key=True)

    # Note: We don't need to explicitly define the backref relationships here, as we have already defined them using backref in the main models.


# Association table for Strain-Flavor relationship
class StrainFlavor(Base):
    __tablename__ = "strain_flavor"

    strain_id = Column(Integer, ForeignKey("strains.id"), primary_key=True)
    flavor_id = Column(Integer, ForeignKey("flavors.id"), primary_key=True)

    # Note: We don't need to explicitly define the backref relationships here, as we have already defined them using backref in the main models.


# Association table for Strain-HelpsWith relationship
class StrainHelpsWith(Base):
    __tablename__ = "strain_helps_with"

    strain_id = Column(Integer, ForeignKey("strains.id"), primary_key=True)
    helps_with_id = Column(Integer, ForeignKey("helps_with.id"), primary_key=True)

    # Note: We don't need to explicitly define the backref relationships here, as we have already defined them using backref in the main models.