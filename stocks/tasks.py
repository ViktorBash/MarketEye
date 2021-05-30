import csv
from webscraper import webscrape
from machine_learning import clean_string, get_sentiment


class StockTask:
    def __init__(self):
        self.stock_list = []
        self.get_stock_list()

    def get_stock_list(self):
        with open("data/spy_list.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.stock_list.append(line['Symbol'])
        csv_file.close()

    def start(self):
        """
        Start the process of webscraping through all the stocks in the stock_list list. Then push the results through
        to machine learning, and write everything to CSV files.
        """
        for stock in self.stock_list:
            # Get the latest tweets
            tweets = webscrape(stock)
            for i in range(len(tweets)):
                tweets[i] = clean_string(tweets[i])
            self.write_to_csv(stock, tweets, "_latest")

            # Get the top tweets
            tweets = webscrape(stock, top_results=True)
            for i in range(len(tweets)):
                tweets[i] = clean_string(tweets[i])
            self.write_to_csv(stock, tweets, "_top")
            print(f"Wrote ${stock} to top & latest")

    @staticmethod
    def write_to_csv(ticker: str, tweets, extra_title=""):
        with open(f"data/stock_name_csv/{ticker.upper()}{extra_title}.csv", "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for tweet in tweets:
                sentiment = get_sentiment(tweet)
                csv_writer.writerow([tweet, sentiment.labels[0].value, sentiment.labels[0].score])
        csv_file.close()


if __name__ == "__main__":
    new_task = StockTask()
    new_task.start()
