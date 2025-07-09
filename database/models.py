from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    operating_hours = Column(String)
    waze_link = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
