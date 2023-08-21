from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Flavor(Base):
    __tablename__ = "flavors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # This relationship will give us flavor.strain_associations to access all associated strain-flavor records
    strain_associations = relationship("StrainFlavor", backref="flavor")
