from dotenv import load_dotenv
import os

env_path = os.path.join(os.getcwd(), 'flightRadar', '.env')
load_dotenv(dotenv_path=env_path)

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")

BOT_NAME = 'flightRadar'
SPIDER_MODULES = ['flightRadar.spiders']
NEWSPIDER_MODULE = 'flightRadar.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'flightRadar.pipelines.FlightradarPipeline': 300,
}

CONNECTION_STRING = 'postgresql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@localhost:5432/flights'
