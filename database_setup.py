import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(250))
    img_url = Column(String(250))

    @property
    def serialize(self):
        return {
            'name'          : self.name,
            'description'   : self.description,
            'id'            : self.id,
            'img_url'       : self.img_url
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    favourite_book_id = Column(String(500))

engine = create_engine("sqlite:///books.db")

Base.metadata.create_all(engine)
