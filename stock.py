#!/usr/bin/env python3

class StockProfile(object):

    def __init__(self, symbol = None, title = None, sector = None, 
            return_on_capital = None, ebit = None, market_cap = None, 
            total_debt = None, cash = None):
        self.symbol = symbol
        self.title = title
        self.sector = sector
        self.return_on_capital = return_on_capital
        self.ebit = ebit
        self.market_cap = market_cap
        self.total_debt = total_debt
        self.cash = cash

    @property
    def earnings_yield(self):

        enterprise_value = (self.market_cap + self.total_debt - self.cash)
        return (self.ebit / enterprise_value)

    def to_string(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
