from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    code = Column(String(100))


engine = create_engine('sqlite:///moredrops.db?check_same_thread=False')
Base.metadata.create_all(engine)