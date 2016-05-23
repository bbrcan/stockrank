import configparser
from database import StockDatabase
from scrapers.scraper import StockScraper
from helpers import sort_list_into_keys


def _rank_stocks(stock_profiles):
    """Ranks stocks by both earnings yield and return on capital.
    Arguments:
    stock_profiles -- A list of stock objects to rank.
    """
    # list of stock symbols, ordered by earnings yield
    by_earnings = sort_list_into_keys(stock_profiles, 'symbol',
                                      'earnings_yield')
    # list of stock symbols, ordered by return on capital
    by_roc = sort_list_into_keys(stock_profiles, 'symbol', 'return_on_capital')

    # rank by sort order for both earnings yield and return on capital
    ranked_stocks = sorted(stock_profiles,
                           key=lambda x: (by_earnings.index(x.symbol) +
                                          by_roc.index(x.symbol)))

    return ranked_stocks


class StockRank(object):
    """Our application's interface, used by main(). Has high-level functions to
    scrape stocks, load them from a database, or print them.
    """
    def __init__(self, config_path):
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

        self._stock_profiles = []
        self._db = StockDatabase(self._config)

    def print_stocks(self):
        """Prints out a list of our stocks, in ranked order, as a fancy table.
        """
        buf = ('%-4s %-6s %-30s %-20s %17s %15s %10s'
               % ('#', 'Symbol', 'Title', 'Sector', 'Market Cap',
                  'Earnings Yield', 'ROC'))
        print(buf)
        print('-' * len(buf))

        for i, stock in enumerate(self._stock_profiles):
            print('%-4d %-6s %-30s %-20s %17s %15.2f %10.2f' %
                  (i+1, stock.symbol, stock.title[:30], stock.sector[:20],
                   '${:,}'.format(stock.market_cap), stock.earnings_yield,
                   stock.return_on_capital))

    def load_local(self):
        """Loads a locally stored copy of the list of stocks.
        """
        self._stock_profiles = _rank_stocks(self._db.get_stock_profiles())

    def download(self):
        """Gets a list of stocks from online sources.

        (Note that at this level of abstraction, the fact that we are actually
        "scraping" is hidden. Hence why this function is named "download()")
        """
        # scrape
        scraper = StockScraper(self._config)
        self._stock_profiles = _rank_stocks(scraper.scrape_stock_profiles())
        # save to db
        self._db.populate(self._stock_profiles)
