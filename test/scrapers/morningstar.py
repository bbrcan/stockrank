#!/usr/bin/env python3

import os
import requests
import unittest
from unittest import mock
from scrapers.morningstar import MorningStarScraper

class MockResponse(object):
    """A mock response returned by Session.get()
    """
    def __init__(self, text):
        self.text = text

class MockSession(object):
    """Mock session object used to retrieve local html files for testing. 
    Functions used to connect to a remote server (mount(), post()) do nothing.
    """
    def mount(self, prefix, adapter):
        pass

    def post(self, url, data=None, json=None, **kwargs):
        pass

    def get(self, url, **kwargs):
        if 'BalanceSheet' in url:
            filename = 'Pharmaxis Ltd - Balance Sheet.html'
        else:
            filename = 'Pharmaxis Ltd - Company Historicals.html'

        filepath = os.path.join('test/assets', filename)

        with open(filepath) as f:
            return MockResponse(f.read())

        raise Exception("No file")

def get_mock_session():
    m = MockSession()

    def _get_mock_session():
        return m

    return _get_mock_session

class MorningStarTests(unittest.TestCase):

    @mock.patch('requests.session', get_mock_session())
    def test_scrape(self):
        scraper = MorningStarScraper('username', 'password')
        stock = scraper.scrape_stock_profile('PXS')
        self.assertEqual(stock.symbol, 'PXS')
        self.assertEqual(stock.title,'Pharmaxis Ltd')
        self.assertEqual(stock.return_on_capital, 0.36)
        self.assertEqual(stock.ebit, 19010000)
        self.assertEqual(stock.market_cap, 69000000)
        self.assertEqual(stock.total_debt, 10893000)
        self.assertEqual(stock.cash, 54138000)
        self.assertEqual(stock.earnings_yield, 0.7381091050281499)

if __name__ == '__main__':
    unittest.main()
