import scrapy


class FlightRadarItem(scrapy.Item):
    date = scrapy.Field()
    start = scrapy.Field()
    stop = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    price = scrapy.Field()
    carrier = scrapy.Field()
