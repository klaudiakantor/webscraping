# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightRadarItem(scrapy.Item):
    date = scrapy.Field()
    start = scrapy.Field()
    stop = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    price = scrapy.Field()
    carrier = scrapy.Field()
