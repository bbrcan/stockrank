import csv
import urllib.request


class AsxScraper(object):
    """Class to scrape stock data from ASX. We use this to grab the sector for
    each stock.
    """
    URL = 'http://www.asx.com.au/asx/research/ASXListedCompanies.csv'

    def __init__(self):
        self._stock_sectors = {}

    def _scrape(self):
        """Scrapes stock data from ASX. To be called only once.
        """

        response = urllib.request.urlopen(self.URL)
        data = response.read().decode('utf-8')

        csv_reader = csv.reader(data.splitlines())

        # skip headers
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)

        for row in csv_reader:
            self._stock_sectors[row[1]] = row[2]

    def sector(self, symbol):
        """Returns the sector for a given stock. On the first run of this
        function, all the stock data will be scraped from ASX. As such, the
        first call will always be slower.
        """
        if not self._stock_sectors:
            self._scrape()

        return self._stock_sectors[symbol]
