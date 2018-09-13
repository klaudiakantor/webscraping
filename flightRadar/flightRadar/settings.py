# -*- coding: utf-8 -*-


# Scrapy settings for flightRadar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from dotenv import load_dotenv
import os

env_path= os.path.join('.','.env')
load_dotenv(dotenv_path=env_path)

DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_NAME = os.getenv("DATABASE_NAME")

BOT_NAME = 'flightRadar'
SPIDER_MODULES = ['flightRadar.spiders']
NEWSPIDER_MODULE = 'flightRadar.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'flightRadar.pipelines.FlightradarPipeline': 300,
}

CONNECTION_STRING = 'postgresql://{}:{}@{}/{}'.format(DATABASE_USER,DATABASE_PASSWORD,DATABASE_HOSTNAME,DATABASE_NAME)
