from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class HelpsWith(Base):
    __tablename__ = "helps_with"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # This relationship will give us helps_with.strain_associations to access all associated strain-helps_with records
    strain_associations = relationship("StrainHelpsWith", backref="helps_with")
