import csv
from webscraper import webscrape
from machine_learning import clean_string, SentimentClass
import time


class StockTask:
    def __init__(self):
        self.stock_list = []
        self.get_stock_list()
        self.sentiment_class = SentimentClass()

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

    def write_to_csv(self, ticker: str, tweets, extra_title=""):
        with open(f"data/stock_name_csv/{ticker.upper()}{extra_title}.csv", "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for tweet in tweets:
                sentiment = self.sentiment_class.get_sentiment(tweet)
                if len(sentiment.labels) > 0:  # If the Sentence model is empty/has no prediction, it will not be added
                    csv_writer.writerow([tweet, sentiment.labels[0].value, sentiment.labels[0].score])
        csv_file.close()


if __name__ == "__main__":
    new_task = StockTask()
    while True:
        new_task.start()
        print("FINISHED, sleeping then restarting")
        # break
        time.sleep(2 * 60 * 60)
