#!/usr/bin/env python3

from stockrank import StockRank

def main():

    # TODO: add command-line options (eg, --scrape, --print)
    stockrank = StockRank()
    stockrank.load()
    stockrank.print_stocks()

if __name__ == '__main__':
    main()
