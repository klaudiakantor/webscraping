from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String

from scrapy.utils.project import get_project_settings
import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Flights(DeclarativeBase):
    __tablename__ = 'flight_table'
    id = Column(Integer, primary_key=True)
    created_at = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d"))

    date = Column('date', String)
    start = Column('start', String(), default=None)
    stop = Column('stop', String(), default=None)
    start_time = Column('start_time', String(), default=None)
    stop_time = Column('end_time', String(), default=None)
    price = Column('price', String(), default=None)
    carrier = Column('carrier', String(), default=None)

    def __init__(self, date, start, stop, start_time, stop_time, price, carrier):
        # self.carrier=carrier

        self.date = date
        self.start = start
        self.stop = stop
        self.start_time = start_time
        self.stop_time = stop_time
        self.price = price
        self.carrier = carrier
