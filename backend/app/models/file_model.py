"""
Database schema for files
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    """File model"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    fingerprint = Column(String)
    watermark = Column(String)
