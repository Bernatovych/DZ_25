from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    degree = Column(String)


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    element = Column(String)
    attribute = Column(String)
    value = Column(String)

engine = create_engine("sqlite:///test.db", pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

