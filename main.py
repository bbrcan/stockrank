#!/usr/bin/env python3

from stockrank import StockRank
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    stockrank = StockRank()

    if args.download:
        stockrank.download()
    else:
        stockrank.load_local()

    if args.show:
        stockrank.print_stocks()

if __name__ == '__main__':
    main()
