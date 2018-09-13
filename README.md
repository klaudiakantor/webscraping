# webscraping

This is a Python project for webscraping of flights' prices from two carriers: Ryanair and Wizzair.

The project consists of two directories (two subprojects):
- flightRadar
- flightWebapp

### flightRadar
The flightRadar directory includes the whole scrapy project. 
To run the spider: 
1. Go to ```webscraping/flightRadar``` 
2. Install all packages listed in ```requirements.txt``` 
3. Create ```.env``` file and define there the username and password for your database (variables' names: DATABASE_USER and DATABASE_PASSWORD).

    Example:
    
      DATABASE_USER = 'my_login'
      
      DATABASE_PASSWORD = 'my_pwd'

4. Run the command: ```scrapy crawl flightsSpider -o fligh.json```

After that, the spider starts working - scraping data from Wizzair and Ryanair webpages - flights prices from next 7 days. There are only flights from Warsaw to Londyn considered. The results (current date, flight date, departure and arrival time, price, carrier and cities' names) are saved in database - PostgreSQL, table: flights.


### flightWebapp
The flightWebapp directory includes the Flask project of web application for browsing the flights' prices. It allows user to search for flights within next 7 days and shows the history of price's changes on a chart.

To run the app:
1. Go to ```webscraping/flightWebapp```
2. Install all packages listed in ```requirements.txt``` 
3. Create ```.env``` file and define there the username and password for your database (variables' names: DATABASE_USER and DATABASE_PASSWORD).

    Example:
    
      DATABASE_USER = 'my_login'
      
      DATABASE_PASSWORD = 'my_pwd'

4. Run the command: ```flask run```

After that, you will get a link in a command line. Copy it and open in the browser.
