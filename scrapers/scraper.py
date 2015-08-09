#!/usr/bin/env python3

import configparser
from scrapers.morningstar import MorningStarScraper
from scrapers.google import GoogleScraper
from scrapers.asx import AsxScraper
from exceptions import FieldMissingException

class StockScraper(object):
    """Used to scrape stock data from a variety of sources on the web. This
    class should be used by the client code instead of the specific scrapers.
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        ms_username = config.get('Credentials', 'morningstar_username')
        ms_password = config.get('Credentials', 'morningstar_password')

        # we only want stocks with market cap > 50,000
        # TODO: add this value to the config file!
        self._google_scraper = GoogleScraper(50000000)
        self._asx_scraper = AsxScraper()
        self._ms_scraper = MorningStarScraper(ms_username, ms_password)
        self._ms_scraper.login()

    def scrape_stock_profiles(self):
        """Scrapes and returns a list of stock profiles from various sources on
        the web.
        """
        stock_profiles = []

        # using Google stock data as our base, populate all the stock profiles
        for stock in self._google_scraper.scrape_stock_profiles():

            try:
                stock.sector = self._asx_scraper.sector(stock.symbol)
            except KeyError:
                # The Google list sometimes has delisted companies, so if a
                # sector can't be found, it's probably been delisted.
                continue

            # TODO: add these values into the config file?
            if 'Utilities' in stock.sector \
                    or 'Financ' in stock.sector \
                    or 'Banks' in stock.sector \
                    or 'Real Estate' in stock.sector:
                        continue

            # Merge in stock data from MorningStar
            # Note that we keep Google's 'market cap', as it's more up-to-date
            try:
                ms_stock = self._ms_scraper.scrape_stock_profile(stock.symbol)
            except FieldMissingException as e:
                print(ms_stock.symbol, str(e))
                # if an attribute can't be found, we can't really do anything
                # other than just continue. some companies don't have 'return on
                # capital' available.
                continue

            stock.return_on_capital = ms_stock.return_on_capital
            stock.ebit = ms_stock.ebit
            stock.total_debt = ms_stock.total_debt
            stock.cash = ms_stock.cash

            stock_profiles.append(stock)

        return stock_profiles
