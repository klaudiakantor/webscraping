from app import db
from sqlalchemy import String, Column, Integer
from datetime import datetime


class Flights(db.Model):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    carrier = Column('carrier', String())
    created_at = Column(String, default=datetime.now().strftime("%Y-%m-%d"))
    date = Column('date', String)
    start = Column('start', String())
    stop = Column('stop', String())
    start_time = Column('start_time', String())
    stop_time = Column('end_time', String())
    price = Column('price', String())

    def __init__(self, date, start, stop, start_time, stop_time, price, carrier):
        self.carrier = carrier
        self.date = date
        self.start = start
        self.stop = stop
        self.start_time = start_time
        self.stop_time = stop_time
        self.price = price

    def __repr__(self):
        return '<id {}>'.format(self.id)
