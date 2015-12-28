from utility import correlation
from data.crawl_price import get_stock_list

STOCK_LIST   = "./data/stock_list.txt"
FILEPATH_RAW = "./data/%s.csv"

if __name__ == "__main__":

    stocks = get_stock_list(STOCK_LIST)
    length = len(stocks)
    cor_result = []

    for i in xrange(length-1):
        for j in xrange(i+1, length):
            file1 = FILEPATH_RAW % stocks[i]
            file2 = FILEPATH_RAW % stocks[j]
            price1 = correlation.open_file(file1)
            price2 = correlation.open_file(file2)
            return1 = correlation.cal_return(price1)
            return2 = correlation.cal_return(price2)

            if correlation.check_timeorder(return1, return2):
                cor = correlation.correlation_of_return(return1, return2)
                cor_result.append([stocks[i], stocks[j], cor])

    cor_result =  sorted(cor_result, key=lambda cor: cor[2])[::-1]

    with file("correlation_report.txt", "wb") as f:
        for cor_record in cor_result:
            data_raw = "%s & %s correlation: %s \n"
            data = data_raw % tuple(cor_record)
            f.write(data)
