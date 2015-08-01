#!/usr/bin/env python3

import urllib.request
import json
from stock import StockProfile
from exceptions import FieldMissingException

class GoogleScraper(object):
    """Class to scrape stock data from Google as a list. Note that the only 
    fields scraped are symbol, market cap and title. We therefore need to 
    combine the Google scraper with other scrapers to populate StockProfile 
    objects fully.
    """
    BASE_URL = 'https://www.google.com/finance'

    def __init__(self, min_market_cap):

        self._request_values =  {
            'output' : 'json',
            'start' : 0,
            'num' : 9999,
            'noIL' : 1,
            'q' : '[currency == "AUD" & (exchange == "ASX")' + \
                   ' & (market_cap >= ' + str(min_market_cap) + ') ]',
            'restype' : 'company'
        }

    def _load_json(self):
        """Sends request to Google and loads the JSON file returned.  The
        contents of this file are returned.
        """
        url_values = urllib.parse.urlencode(self._request_values, False)
        url_values = url_values.replace('%5B', '[')
        url_values = url_values.replace('%5D', ']')
        full_url = self.BASE_URL + '?' + url_values
        response = urllib.request.urlopen(full_url)
        return response.read().decode('utf-8')

    def _scrape_field(self, columns, title):
        """Scrapes an individual field from the JSON file.

        Arguments:
        columns -- A JSON element containing our field.
        title -- The title of the field to scrape.
        """
        for col in columns:

            # a '-' means no result
            if col['field'] == title and col['value'] != '-':
                return col['value']

        raise FieldMissingException('field "' + title + '" missing')

    def _scrape_market_cap(self, columns):
        """Scrapes the market cap field from the JSON. As the field is in format
        '50M', '10B', etc, we need to convert it to a valid integral value.
        """
        market_cap = self._scrape_field(columns, 'MarketCap')

        if 'B' in market_cap:
            market_cap = float(market_cap.strip('B'))
            market_cap = int(market_cap * 1000000000)
        elif 'M' in market_cap:
            market_cap = float(market_cap.strip('M'))
            market_cap = int(market_cap * 1000000)

        return market_cap

    def scrape_stock_profiles(self):
        """Scrapes and returns stock profiles from Google. Note that the only
        fields scraped the symbol, market cap and title.
        """
        data = self._load_json()
        data = data.replace('\\x', '\\u00')
        json_data = json.loads(data)

        stock_profiles = []

        for result in json_data['searchresults']:

            symbol = result['ticker']
            title = result['title']
            market_cap = self._scrape_market_cap(result['columns'])


            stock_profile = StockProfile(symbol = symbol, title = title, 
                    market_cap = market_cap)

            stock_profiles.append(stock_profile)

        return stock_profiles
    
