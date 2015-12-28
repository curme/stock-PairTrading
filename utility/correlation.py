# -*- coding: utf-8 -*-
'''
    MEMO
    2015-12-28
    Calculate the correlation_of_return under the indicators of the following
webpage "http://www.wikihow.com/Calculate-Stock-Correlation-Coefficient".
'''

import math

APPLE_FILE = "../data/apple.csv"
GOOGLE_FILE= "../data/google.csv"

def open_file(filepath):

    data = []
    with file(filepath, "r") as f:
        for line in f:
            line_split = line.split(',')
            data.append([line_split[i] for i in [0, 4]])

    return data[1:] # to kick out the file line "Data, Closing"

def cal_return(stock):

    returns = []
    for i in xrange(1,len(stock)):
        tmp = [stock[i][0]]
        price_t = float(stock[i][1])
        price_l = float(stock[i-1][1])
        return_t= math.log(price_t/price_l, math.e)
        tmp.append(return_t)
        returns.append(tmp)

    return returns

def check_timeorder(stock1, stock2):

    # to check if two stocks have equivalent time stretch
    if len(stock1) != len(stock2): return False

    # to check if two stocks have same time order
    flag = False
    for i in xrange(len(stock1)): 
        if stock1[i][0] != stock2[i][0]: flag &= True
    return False if flag else True

def correlation_of_return(stock1, stock2):

    # step 1: calculate the means
    time_len = len(stock1) # because two stocks share same time stretch
    mean_stock1, mean_stock2 = 0, 0
    for record in stock1: mean_stock1 += float(record[1])/time_len
    for record in stock2: mean_stock2 += float(record[1])/time_len

    # step 2: calculate the variance, standard deviation, and covirance
    variance_stock1, variance_stock2 = 0, 0
    for r in stock1: variance_stock1 += (float(r[1])-mean_stock1) ** 2 /time_len
    for r in stock2: variance_stock2 += (float(r[1])-mean_stock2) ** 2 /time_len
    s_deviation_stock1, s_deviation_stock2 = 0, 0
    s_deviation_stock1 = variance_stock1 ** 0.5
    s_deviation_stock2 = variance_stock2 ** 0.5
    covirance = 0
    for i in xrange(time_len):
        covirance += \
        (float(stock1[i][1])-mean_stock1) * (float(stock2[i][1])-mean_stock2) \
        / time_len

    # step 3: calculate correlation
    correlation = covirance / (s_deviation_stock1 * s_deviation_stock2)

    return correlation

if __name__ == "__main__":

    stocks = crawl_price.get_stock_list()
    print stocks

    apple_price   = open_file(APPLE_FILE)
    google_price  = open_file(GOOGLE_FILE)
    apple_return  = cal_return(apple_price)
    google_return = cal_return(google_price)

    if check_timeorder(apple_return, google_return):
        correlation= correlation_of_return(apple_return, google_return)
        print correlation
