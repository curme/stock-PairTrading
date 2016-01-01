import time
import requests

RAW_LINK = "http://real-chart.finance.yahoo.com/table.csv?" + \
           "s=%s&a=11&b=27&c=2012&d=11&e=28&f=2015&g=d&ignore=.csv"
STOCK_LIST = "stock_list.txt"

def price_crawl(code):

    target_link =  RAW_LINK % code
    try:    response = requests.get(target_link)
    except: 
        print code
        return
    with file("%s.csv" % code, "wb") as f:
        f.write(response.content)
        print code, ".csv lines: ", len(response.content.split("\n"))

def get_stock_list(filepath):

    stocks = []
    with file(filepath, "r") as f:
        for line in f: stocks.append(line.split(" ")[2][1:])

    return stocks

if __name__ == "__main__":

    stocks = get_stock_list(STOCK_LIST)
    for stock in stocks[62:]:
        price_crawl(stock)
