# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from flightRadar.flights import Flights, db_connect, create_table


class FlightradarPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        date = item["date"]
        start = item["start"]
        stop = item["stop"]
        start_time = item["start_time"]
        end_time = item["end_time"]
        price = item["price"]
        carrier = item["carrier"]
        db = Flights(date, start, stop, start_time, end_time, price, carrier)

        try:
            session.add(db)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
