import time
import requests

RAW_LINK = "http://real-chart.finance.yahoo.com/table.csv?" + \
           "s=%s&a=11&b=27&c=2014&d=11&e=28&f=2015&g=d&ignore=.csv"

def price_crawl(code):

    target_link =  RAW_LINK % code
    response = requests.get(target_link)
    with file("%s.csv" % code, "wb") as f:
        f.write(response.content)
        print code, ".csv lines: ", len(response.content.split("\n"))

def get_stock_list():

    stocks = []
    with file("stock_list.txt", "r") as f:
        for line in f: stocks.append(line.split(" ")[2][1:])

    return stocks

if __name__ == "__main__":

    stocks = get_stock_list()
    for stock in stocks[65:]:
        #if stock == "2318.HK": continue # this stock cannot receive data, skip
        print stock
        price_crawl(stock)
