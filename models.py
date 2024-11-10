from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, unique=True, nullable=False)

engine = create_engine('sqlite:///pokarm.db')
Base.metadata.create_all(engine)
