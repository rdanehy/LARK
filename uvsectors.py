from yfapi import YahooFinanceAPI
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ticker -> description dict (place new tickers here)
sector_tickers = {
    "XRT": "Retail",
    "SOXX": "Semiconductors",
    "VDE": "Energy",
    "VHT": "Health Care"
}
# just in case these change
price_column = "Close"
date_column = "Date"

api = YahooFinanceAPI()
sp_data = api.get_ticker_data("spy", datetime.datetime(2010, 1, 1), datetime.datetime(2020, 12, 31))
normal_sp_close = (sp_data[price_column] - sp_data[price_column].min())/ \
                  (sp_data[price_column].max() - sp_data[price_column].min())

for key in sector_tickers:
    ticker, desc = key, sector_tickers[key]
    comp_data = api.get_ticker_data(ticker, datetime.datetime(2010, 1, 1), datetime.datetime(2020, 12, 31))
    normal_comp_data = (comp_data[price_column] - comp_data[price_column].min())/ \
                       (comp_data[price_column].max() - comp_data[price_column].min())
    divergence = normal_comp_data - normal_sp_close

    ## Divergence = 0 -> no divergence between S&P and Sector (or stock)
    ## Divergence < 0 -> sector gains less than S&P gains (sector may be undervalued)
    ## Divergence > 0 -> sector gains greater than S&P gains (sector may be overvalued)
    div, = plt.plot(comp_data[date_column], divergence, label="Divergence")
    sp, = plt.plot(sp_data[date_column], normal_sp_close, label="SPY - S&P 500")
    comp, = plt.plot(comp_data[date_column], normal_comp_data, label="{} - {}".format(ticker, desc))
    plt.legend(handles=[div, sp, comp])
    plt.axhline(0, color="black")
    plt.savefig("./plots/{}.png".format(ticker))
    plt.clf()