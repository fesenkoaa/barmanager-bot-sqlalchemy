from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Query
from config import data_password, username
from creator_models import Drinks, Store, Recipes, GuestTable

engine = create_engine(f'postgresql://{username}:{data_password}@localhost:5432/barmanager')

Session = sessionmaker(bind=engine)
session = Session()


def add_order(table_id: int, drink: str, drinks_amount: int):
    drinks_items = session.query(Drinks).filter(Drinks.name == f'{drink}').first()
    get_amount = session.query(Recipes).filter(Recipes.drinks_id == drinks_items.id).all()

    for el in get_amount:
        res = lambda x: x * drinks_amount
        session.query(Store).filter(Store.id == el.store_id).update({Store.amount: Store.amount - el.amount},
                                                                    synchronize_session=False)
        session.commit()
        # print(el.store_id, res(el.amount))

    add_one = GuestTable(drink=f'{drink}', amount=drinks_amount, table_id=table_id, price=drinks_items.price)
    session.add(add_one)
    session.commit()
    print(f'You have ordered {drinks_amount} {drink} to table #{table_id}!')


def del_from_gtable(table_id: int, drink: str):
    session.query(GuestTable).filter(and_(GuestTable.table_id == table_id), (GuestTable.drink == f'{drink}')).delete()
    session.commit()
    return f'You have deleted all {drink} from table #{table_id}!'


def del_gtable(table_id: int):
    session.query(GuestTable).filter(GuestTable.table_id == table_id).delete()
    session.commit()
    return f'You have cleared table #{table_id}!'


def get_bill(table_id: int):
    bill = session.query(GuestTable).filter(GuestTable.table_id == table_id).all()
    for row in bill:
        print(row.drink, row.amount, row.price)
    session.query(GuestTable).filter(GuestTable.table_id == table_id).delete()
    session.commit()
    return f'Bill for table #{table_id} is printed!'


def add_store(name: str, amount: float, type='some type'):
    add = Store(name=name, amount=amount, type=type)
    session.add(add)
    session.commit()
    return f'You\'ve added {amount} l of {name} to store.'


def store_subtract(name: str, amount: float):
    session.query(Store).filter(Store.name == f'{name}').update({Store.amount: Store.amount - amount},
                                                                synchronize_session=False)
    session.commit()
    return f'You have subtracted {amount} {name} from store. The amount is updated!'


def store_subjoin(name: str, amount: float):
    session.query(Store).filter(Store.name == f'{name}').update({Store.amount: Store.amount + amount},
                                                                synchronize_session=False)
    session.commit()
    return f'You have subjoin {amount} {name} from store. The amount is updated!'


def delete_from_store(name: str):
    session.query(Store).filter(Store.name == f'{name}').delete()
    session.commit()
    return f'You have deleted {name} from store!'
