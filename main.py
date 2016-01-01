import pandas
from utility import plot
from utility import regression
from utility import correlation
from data.crawl_price import get_stock_list

STOCK_LIST   = "./data/stock_list.txt"
FILEPATH_RAW = "./data/%s.csv"

def generate_correlation_report():

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

def draw_scatter(stock1, stock2):

    stock1_data = pandas.DataFrame.from_csv(FILEPATH_RAW % stock1)
    stock2_data = pandas.DataFrame.from_csv(FILEPATH_RAW % stock2)

    key = "Adj Close"
    data = pandas.DataFrame(index=stock1_data.index)
    data[stock1], data[stock2] = stock1_data[key], stock2_data[key]

    # plot scatter plot
    plot.plot_scatter_series(data, stock1, stock2)

def get_lineal_regression(stock1, stock2):

    stock1_price = correlation.open_file(FILEPATH_RAW % stock1)
    stock2_price = correlation.open_file(FILEPATH_RAW % stock2)

    if correlation.check_timeorder(stock1_price, stock2_price):
        return regression.cal_lineal_regression(stock1_price, stock2_price)

    return None, None

if __name__ == "__main__":

    generate_correlation_report()
'''
    with file("correlation_report.txt", "r") as f:

        stock1, stock2 = "", ""
        for line in f:
            tokens = line.split(" ")
            if float(tokens[-2]) < 0.9: 
                stock1, stock2 = tokens[0], tokens[2]
                break

        print stock1, stock2

        # draw scatter
        draw_scatter(stock1, stock2)

        # calculate lineal regression equation
        # ln(PriceY_t) = Gamma*ln(PriceX_t) + Mu)
        gamma, mu = get_lineal_regression(stock1, stock2)
        print gamma, mu'''
