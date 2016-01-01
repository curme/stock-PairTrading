# -*- coding: utf-8 -*-
'''
    MEMO
    2015-12-29
    the lineal regression equation: ln(PriceY_t) = Gamma*ln(PriceX_t) + Mu
'''

import math
import correlation

def cal_lineal_regression(prices_x, prices_y):

    # step 1: preparation
    ln_prices_x, ln_prices_y = [], []
    for item in prices_x[60:150]: ln_prices_x.append(math.log(float(item[1]), math.e))
    for item in prices_y[60:150]: ln_prices_y.append(math.log(float(item[1]), math.e))

    length = len(ln_prices_x) # and ln_return_y must share same length
    mean_x, mean_y = 0.0, 0.0
    for r in ln_prices_x: mean_x += r / length
    for r in ln_prices_y: mean_y += r / length

    virance_x, covirance = 0.0, 0.0
    for r in ln_prices_x: virance_x += (r-mean_x) ** 2 / length
    for i in xrange(length):
        covirance += (ln_prices_x[i]-mean_x) * (ln_prices_y[i]-mean_y) / length

    # step 2: calculate gamma, gamma = cov / v_x
    gamma = covirance / virance_x

    # step 3: calculate mu, mu = mean_y - gamma * mean_x
    mu = mean_y - gamma * mean_x

    for i in xrange(length):
        print ln_prices_y[i] - (gamma*ln_prices_x[i] + mu)

    return gamma, mu

if __name__ == "__main__":

    apple_path = correlation.APPLE_FILE
    google_path= correlation.GOOGLE_FILE

    apple_price = correlation.open_file(apple_path)
    google_price= correlation.open_file(google_path)
    apple_return = correlation.cal_return(apple_price)
    google_return= correlation.cal_return(google_price)

    if correlation.check_timeorder(apple_price, google_price):
        gamma, mu = cal_lineal_regression(apple_price, google_price)
        print gamma, mu
