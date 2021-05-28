import yfinance as yf
import pandas as pd


def get_latest_stock_price(ticker: str):
    ticker_yf = yf.Ticker(ticker)
    return ticker_yf.info['ask']


def get_spy_list():
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    table = table[0]
    data = pd.DataFrame(data=table["Symbol"])
    data.to_csv("data/spy_list.csv", index=False, header=True)


if __name__ == "__main__":
    # Example call
    # print(get_latest_stock_price("TSLA"))
    get_spy_list()
