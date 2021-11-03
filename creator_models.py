from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import data_password, username

engine = create_engine(f'postgresql://{username}:{data_password}@localhost:5432/barmanager')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Drinks(Base):  # created
    __tablename__ = 'drinks'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)

    cocktails = relationship("Recipes", back_populates="drinks")


class Store(Base):  # created
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(50))
    amount = Column(Numeric())

    storehouse = relationship("Recipes", back_populates="store")


class Recipes(Base):  # created
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)  # didn't create without id column
    drinks_id = Column(Integer, ForeignKey('drinks.id'))
    store_id = Column(Integer, ForeignKey('store.id'))
    amount = Column(Numeric())

    drinks = relationship('Drinks', back_populates='cocktails')
    store = relationship('Store', back_populates='storehouse')


class GuestTable(Base):  # created
    __tablename__ = 'guest_table'

    id = Column(Integer, primary_key=True)
    drink = Column(String(50))
    amount = Column(Integer)
    price = Column(Integer)
    table_id = Column(Integer)


# Base.metadata.create_all(engine)

