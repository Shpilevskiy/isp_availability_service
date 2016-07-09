from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ISP(Base):
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    url = Column(String(100), unique=True)

    connections = relationship('Connection', back_populates='isp')


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    status = Column(String(100), nullable=False)

    connections = relationship('Connection', back_populates='status')


class Connection(Base):
    __tablename__ = 'connection'
    id = Column(Integer, primary_key=True)

    isp_id = Column(Integer, ForeignKey('provider.id'))
    isp = relationship('ISP', back_populates='connections')

    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship('Status', back_populates="connections")

    region = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    street = Column(String(100), nullable=False, index=True)
    house_number = Column(String(100), nullable=False, index=True)