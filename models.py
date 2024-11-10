from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    name_test = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

engine = create_engine('sqlite:///pokarm.db')
