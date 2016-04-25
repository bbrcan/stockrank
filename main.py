#!/usr/bin/env python3

from stockrank import StockRank
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true', 
            help='download stock data and store locally')
    parser.add_argument('--show', action='store_true',
            help='prints a list of stocks, in ranked order')
    parser.add_argument('--config', type=str, default='config.ini',
            help='specifies the path to the config file')
    args = parser.parse_args()

    stockrank = StockRank(args.config)

    if args.download:
        stockrank.download()
    else:
        stockrank.load_local()

    if args.show:
        stockrank.print_stocks()

if __name__ == '__main__':
    main()
