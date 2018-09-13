import scrapy
import time
from selenium import webdriver
import datetime
import re
import dateparser
from scrapy import signals
from flightRadar.items import FlightRadarItem


class FlightsSpider(scrapy.Spider):
    name = "flightsSpider"
    allowed_domains = ["ryanair.com", "wizzair.com"]
    now = datetime.datetime.now()

    urls = []
    for i in range(1,8):
        day = datetime.datetime.strftime(now + datetime.timedelta(days=i), "%Y-%m-%d")
        ryanair = 'https://www.ryanair.com/pl/pl/booking/home/WMI/STN/{}//1/0/0/0'.format(day)
        urls.append(ryanair)
        wizzair = 'https://wizzair.com/pl-pl#/booking/select-flight/WAW/LTN/{}/null/1/0/0/0/null'.format(day)
        urls.append(wizzair)

    wizzair_date_button = '//*[@id="search-departure-date"]'
    wizzair_arrival = 'Londyn-Luton'
    wizzair_departure = 'Warszawa - Chopin'
    wizzair_start = '//*[@id="search-departure-station"]'
    wizzair_stop = '//*[@id="search-arrival-station"]'
    wizzair_btn_ok = '//*[@id="flight-search"]/div/div/div[3]/form/div[4]/button/span'
    wizzair_confirm_depart = '//*[@id="flight-search"]/div/div/div[3]/form/div[1]/fieldset/div[3]/div/div[3]/div[1]/label/strong/mark'
    wizzair_confirm_arriv = '//*[@id="flight-search"]/div/div/div[3]/form/div[1]/fieldset/div[3]/div/div[3]/div[1]/label/strong/mark'
    wizzair_price = '//strong[@class="rf-fare__price__current"]'
    wizzair_time = '//td[@class="booking-flow__prices-table__content__column booking-flow__prices-table__content__column--time"]'
    ryanair_start = '//*[@id="outbound"]/form/div[3]/div/flights-table/div/div[1]/div[1]/flights-table-header/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/span[1]'
    ryanair_start_time = '//*[@id="outbound"]/form/div[3]/div/flights-table/div/div[1]/div[1]/flights-table-header/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]'
    ryanair_end_time = '//*[@id="outbound"]/form/div[3]/div/flights-table/div/div[1]/div[1]/flights-table-header/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]'
    ryanair_stop = '//*[@id="outbound"]/form/div[3]/div/flights-table/div/div[1]/div[1]/flights-table-header/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/span[2]'
    ryanair_price = '//*[@id="outbound"]/form/div[3]/div/flights-table/div/div[1]/div[1]/flights-table-header/div[1]/div[2]/flights-table-price/div[1]/div[1]/div[contains(@class,"core-btn-primary")]/span[contains(@class, "flights-table-price__price")]'

    def __init__(self, *args, **kwargs):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=chromeOptions)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FlightsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        for url in self.urls:
            date = re.findall(r'\d\d\d\d\-\d\d\-\d\d', url)[0]
            yield scrapy.Request(url=url, callback=self.parse, meta={'date': date}, dont_filter=True)

    def parse(self, response):
        self.driver.set_window_size(1024, 768)
        self.driver.maximize_window()

        self.driver.get(response.url)
        time.sleep(60)
        flight = FlightRadarItem()
        carrier = re.findall(r'(\w+)(?:\.com)', response.url)[0]
        date = response.meta['date']

        if carrier == 'wizzair':
            proper_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            day = proper_date.day
            month = proper_date.month - 1
            year = proper_date.year
            wizzair_day_button = '//button[@class="pika-button pika-day"][@data-pika-year="{}"][@data-pika-month="{}"][@data-pika-day="{}"]'.format(
                year, month, day)

            from_airport = self.driver.find_element_by_xpath(self.wizzair_start)
            from_airport.clear()
            from_airport.send_keys(self.wizzair_departure)

            wizzair_from_confirm = self.driver.find_element_by_xpath(self.wizzair_confirm_depart)
            wizzair_from_confirm.click()

            to_airport = self.driver.find_element_by_xpath(self.wizzair_stop)
            to_airport.clear()
            to_airport.send_keys(self.wizzair_arrival)
            to_confirm = self.driver.find_element_by_xpath(self.wizzair_confirm_arriv)
            to_confirm.click()

            button = self.driver.find_element_by_xpath(self.wizzair_date_button)
            button.click()
            time.sleep(20)

            select_date = self.driver.find_element_by_xpath(wizzair_day_button)
            select_date.click()
            time.sleep(20)

            container = self.driver.find_element_by_xpath(self.wizzair_btn_ok)
            container.click()
            time.sleep(40)

            window_before = self.driver.window_handles[-2]
            self.driver.switch_to_window(window_before)
            self.driver.close()
            window_after = self.driver.window_handles[-1]
            self.driver.switch_to_window(window_after)

            flight['price'] = str(self.driver.find_element_by_xpath(self.wizzair_price).text).replace('zł', '').replace(
                ' ', '')
            flight['start'] = self.wizzair_departure
            flight['stop'] = self.wizzair_arrival
            flight['carrier'] = carrier
            date_time = self.driver.find_element_by_xpath(self.wizzair_time).text
            times = re.findall(r'\d\d:\d\d', date_time)
            flight['start_time'] = times[0]
            flight['end_time'] = times[1]
            data = re.findall(r'(?:\, )(\d+ \w+ \d\d\d\d)', date_time)[0]
            flight['date'] = dateparser.parse(data).date()


        elif carrier == 'ryanair':
            flight['carrier'] = carrier
            flight['date'] = date
            flight['start'] = self.driver.find_element_by_xpath(self.ryanair_start).text
            flight['stop'] = self.driver.find_element_by_xpath(self.ryanair_stop).text
            flight['start_time'] = self.driver.find_element_by_xpath(self.ryanair_start_time).text
            flight['end_time'] = self.driver.find_element_by_xpath(self.ryanair_end_time).text
            flight['price'] = str(self.driver.find_element_by_xpath(self.ryanair_price).text).replace(' ', '').replace(
                'zł', '').replace(',','.')
        else:
            print("***Operation failed****")
            raise Exception('ERROR: Could not extract carrier name')

        yield flight

    def spider_closed(self):
        self.driver.quit()
