#!/usr/bin/env python3

import sqlite3 
from stock import StockProfile

class StockDatabase(object):
    """Class used to manage the storage and retrieval of stock data from an
    underlying database.
    """
    def __init__(self, config):
        db = sqlite3.connect(config.get('Application', 'database_path'))
        db.execute('CREATE TABLE IF NOT EXISTS stocks ' 
                '(symbol TEXT,'
                'title TEXT,'
                'sector TEXT,'
                'return_on_capital REAL,'
                'ebit REAL,'
                'market_cap INTEGER,'
                'total_debt INTEGER,'
                'cash INTEGER)')

        db.commit()
        db.row_factory = sqlite3.Row
        self._db = db
        self._cursor = db.cursor()

    def empty(self):
        """Returns True if no stock data is present in the database, otherwise
        False.
        """
        self._cursor.execute('SELECT count(*) FROM stocks')
        row = self._cursor.fetchone()

        if row[0] is 0:
            return True

        return False

    def populate(self, stock_profiles):
        """Populates the database with given stock data.

        Arguments:
        stock_profiles -- A list of StockProfile objects.
        """
        self._cursor.execute('DELETE FROM stocks')

        # store values to insert into the DB here first, so we can insert them
        # all at once using the more efficient executemany()
        many_values = []

        for stock in stock_profiles:

            many_values.append([
                stock.symbol, 
                stock.title,
                stock.sector, 
                stock.return_on_capital,
                stock.ebit,
                stock.market_cap,
                stock.total_debt,
                stock.cash
                ])

        self._cursor.executemany('INSERT INTO stocks VALUES ' \
                '(?, ?, ?, ?, ?, ?, ?, ?)', many_values)
        self._db.commit()

    def get_stock_profiles(self):
        """Returns a list of StockProfile objects, pulled from the database.
        """
        stock_profiles = []
        self._cursor.execute('SELECT * FROM stocks')

        for row in self._cursor.fetchall():
            stock_profiles.append(StockProfile(
                symbol = row['symbol'], 
                title = row['title'], 
                sector = row['sector'], 
                return_on_capital = row['return_on_capital'], 
                ebit = row['ebit'],
                market_cap = row['market_cap'],
                total_debt = row['total_debt'],
                cash = row['cash']))

        return stock_profiles
