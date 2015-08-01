#!/usr/bin/env python3

import time
import re
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
from stock import StockProfile
import random
from helpers import timestamp
from exceptions import FieldMissingException

class MorningStarScraper(object):
    """Class used to scrape stock data from MorningStar. login() must be called
    prior to scrape_stock_profile(). The only fields scraped will are symbol,
    title, market cap, return on capital, ebit, total debt, and cash.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._cookie_jar = http.cookiejar.CookieJar()
        self._url_opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self._cookie_jar))

    def login(self):
        """Logs into MorningStar, so members-only pages can be loaded. This must
        be run before scrape_stock_profile().
        """
        url = 'http://www.morningstar.com.au/Security/Login'

        values = {'UserName': self.username, 'Password': self.password }
        data = urllib.parse.urlencode(values)
        binary_data = data.encode('utf-8')
        self._url_opener.open(url, binary_data)

    def scrape_stock_profile(self, symbol):
        """Scrapes MorningStar and returns a StockProfile object.

        Arguments:
        symbol -- ASX symbol of the company we want to scrape, eg "CBA".
        """
    
        scraper = _MorningStarStockScraper(self._url_opener, symbol)
        return scraper.scrape()

class _MorningStarStockScraper(object):
    """Class to scrape data from MorningStar for an individual stock. Should
    only be used by the MorningStarScraper() class.
    """
    _SLEEP_MAX = 5.0
    BALANCE_SHEET_URL = 'http://www.morningstar.com.au/Stocks/BalanceSheet/'
    HISTORICALS_URL = 'http://www.morningstar.com.au/Stocks/CompanyHistoricals/'

    _last_scrape = 0

    def __init__(self, url_opener, symbol):
        self._url_opener = url_opener 
        self._stock_profile = StockProfile(symbol)

    def _delay_scrape(self):
        """Sleeps for a random amount of time, between 0 and _SLEEP_MAX. Should 
        be called before every page request, so that not too many requests are
        sent at once.
        """
        if self._last_scrape > 0:
            time.sleep(random.uniform(0.0, self._SLEEP_MAX))

        self._last_scrape = timestamp()

    def _scrape_field(self, parent, title):
        """Scrapes a specific field from a page. When there are multiple years
        for a field, the last available year is always chosen.

        Arguments:
        parent -- A BeautifulSoup element. We look for our field inside it.
        title -- The title of the field, eg 'Return on capital'.
        """
        print('_scrape_field','title:',title)

        # use regex so we don't have to be so exact in our title searches
        pattern = re.compile(r'' + title + '.*')
        prev_element = next_element = parent.find('td', text = pattern)

        if not prev_element:
            raise FieldMissingException('field "' + title + '" missing')

        # find the last TD sibling; it will have the latest year's results
        while next_element:

            if hasattr(next_element, 'text'):
                prev_element = next_element

            next_element = next_element.next_sibling

        text = prev_element.text
        # some fields have a comma, eg '4,873.0'
        text = text.strip().replace(',', '')

        if text == '--':
            raise FieldMissingException('field "' + title + '" missing')

        return float(text)

    def _scrape_title(self, parent):
        """Scrapes the company title - eg, 'Commonwealth Bank of Australia'.
        This information comes from the BalanceSheet page.
        """
        self._delay_scrape()

        div = parent.find('div', { 'class' : 'N_QHeaderContainer' })
        label = div.find('label')
        self._stock_profile.title = label.text.strip()

    def _scrape_balancesheet(self):
        """Scrapes data from the BalanceSheet page.
        """
        self._delay_scrape()

        url = self.BALANCE_SHEET_URL + self._stock_profile.symbol
        soup = BeautifulSoup(self._url_opener.open(url))

        self._scrape_title(soup)

        # the div doesn't have any unique identifiers, but we know it appears 
        # after this anchor
        anchor = soup.find('a', { 'name': 'CapitalPosition' })
        div = anchor.parent

        raw_cash = self._scrape_field(div, 'Cash')
        raw_total_debt = self._scrape_field(div, 'Total debt')

        # data displayed in thousands, so multiply for full number
        self._stock_profile.cash = int(raw_cash * 1000) 
        self._stock_profile.total_debt = int(raw_total_debt * 1000)

    def _scrape_historicals(self):
        """Scrapes data from the HistoricalFinancials page.
        """
        self._delay_scrape()

        url = self.HISTORICALS_URL + self._stock_profile.symbol
        soup = BeautifulSoup(self._url_opener.open(url))

        parent = soup.find('div', { 'id' : 'HistoricalFinancialsTab' })
        raw_roc = self._scrape_field(parent, 'Return on capital')
        raw_ebit = self._scrape_field(parent, 'EBIT')

        parent = soup.find('div', { 'id' : 'PerShareStatisticsTab' })
        raw_market_cap = self._scrape_field(parent, 'Market cap')

        # convert from percentage to decimal
        self._stock_profile.return_on_capital = raw_roc / 100.0

        # data displayed in millions, so multiply for full number
        self._stock_profile.ebit = int(raw_ebit * 1000000)
        self._stock_profile.market_cap = int(raw_market_cap * 1000000)

    def scrape(self):
        """Scrapes MorningStar and returns a StockProfile object.
        """
        print('scrape','symbol:',self._stock_profile.symbol)
        self._scrape_historicals()
        self._scrape_balancesheet()
        return self._stock_profile
