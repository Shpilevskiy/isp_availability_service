from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class City(Base):
    __tablename__ = 'City'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(30), unique=True, nullable=False, index=True)
