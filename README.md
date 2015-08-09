## StockRank 

The program seeks to implement the magic formula from Joel Greenblatt's book 
'The Little Book That Beats The Market' on the Australian Stock Exchange (ASX).

You can read more about magic formula investing here:

https://en.wikipedia.org/wiki/Magic_formula_investing

It scrapes data from a variety of sources and stores it an Sqlite database. It
then sorts the results according to the magic formula and prints out the 
results.

## Sources

My current sources are:

* Google - for a list of stocks and their current market caps
* ASX - for stock sector information
* MorningStar - for the previous year's financial data

## TODO:

* Add command-line options (one to scrape data, one to print data)
* Add database path to config file
* Add market cap to config file
* Add sector filters to config file
* Look at using Herald Sun stock data instead (doesn't require user login)

## Disclaimer

Use at your own risk! I'm a programmer, not a professional investor. I would
therefore advise anyone looking to use this program to examine the data that I
have obtained, and how I use it (and then let me know if you find any errors!).

