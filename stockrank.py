#!/usr/bin/env python3

from database import StockDatabase
from scrapers.scraper import StockScraper
from helpers import sort_list_into_keys

def _rank_stocks(stock_profiles):

    # list of stock symbols, ordered by earnings yield
    by_earnings = sort_list_into_keys(stock_profiles, 'symbol', 
            'earnings_yield')
    # list of stock symbols, ordered by return on capital
    by_roc = sort_list_into_keys(stock_profiles, 'symbol', 'return_on_capital')

    # rank by sort order for both earnings yield and return on capital
    ranked_stocks = sorted(stock_profiles, key = lambda x : 
            (by_earnings.index(x.symbol) + by_roc.index(x.symbol)))

    return ranked_stocks

class StockRank(object):

    def __init__(self):
        self._stock_profiles = []

    def print_stocks(self):

        buf = ('%-4s %-6s %-30s %-20s %17s %15s %10s' 
                % ('#', 'Symbol', 'Title', 'Sector', 'Market Cap', 
                    'Earnings Yield', 'ROC'))
        print(buf)
        print('-' * len(buf))
        i = 1

        for stock in self._stock_profiles:
            print('%-4d %-6s %-30s %-20s %17s %15.2f %10.2f' 
                    % (i, stock.symbol, stock.title[:30], stock.sector[:20],
                        '${:,}'.format(stock.market_cap), stock.earnings_yield,
                        stock.return_on_capital))
            i += 1

    def load(self):

        db = StockDatabase()

        if not db.empty():
            self._stock_profiles = _rank_stocks(db.get_stock_profiles())
            return

        scraper = StockScraper()
        self._stock_profiles = _rank_stocks(scraper.scrape_stock_profiles())

        db.populate(self._stock_profiles)

