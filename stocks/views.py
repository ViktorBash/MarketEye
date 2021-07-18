from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockSearchForm
from .stock_information import get_latest_stock_price
import os
import csv
from django.conf import settings

def home(request):
    """Home page view that handles what users see when they visit the website. Home page contains a form to search
    for a stock. """
    if request.method == "POST":
        form = StockSearchForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            return redirect("ticker", ticker=ticker)
    else:
        form = StockSearchForm()
    return render(request, "home.html", {"form": form})


def stock_sticker(request, ticker: str):
    """
    Search for a specific stock via a Django parameter in the URL. Connects business logic (webscraping,
    machine learning, etc) to what the webpage serves.
    """
    # Check if ticker is in stock list (S&P 500 is the list at the moment)
    pass_check_1 = False
    with open(os.path.join(settings.BASE_DIR, "stocks/data/spy_list.csv"), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if line['Symbol'] == ticker:
                pass_check_1 = True
    csv_file.close()

    if not pass_check_1:
        return redirect("home")

    # All checks are passed by this point 🚀 🚀 🚀
    latest_tweets_pos = 0
    latest_tweets_neg = 0
    latest_tweets_sentiment = ""

    with open(os.path.join(settings.BASE_DIR, f"stocks/data/stock_name_csv/{ticker}_latest.csv"), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['Tweet', 'Sentiment', 'Confidence'])
        for line in csv_reader:
            if line['Sentiment'] == "NEGATIVE":
                latest_tweets_neg += 1
            else:
                latest_tweets_pos += 1
    csv_file.close()

    if latest_tweets_pos > latest_tweets_neg:
        latest_tweets_sentiment = "Positive"
    elif latest_tweets_neg > latest_tweets_pos:
        latest_tweets_sentiment = "Negative"
    else:
        latest_tweets_sentiment = "Neutral"

    top_tweets_pos = 0
    top_tweets_neg = 0
    top_tweets_sentiment = ""

    with open(os.path.join(settings.BASE_DIR, f"stocks/data/stock_name_csv/{ticker}_top.csv"), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['Tweet', 'Sentiment', 'Confidence'])
        for line in csv_reader:
            if line['Sentiment'] == "NEGATIVE":
                top_tweets_neg += 1
            else:
                top_tweets_pos += 1
    csv_file.close()

    if top_tweets_pos > top_tweets_neg:
        top_tweets_sentiment = "Positive"
    elif top_tweets_neg > top_tweets_pos:
        top_tweets_sentiment = "Negative"
    else:
        top_tweets_sentiment = "Neutral"

    stock_price = get_latest_stock_price(ticker)

    return render(request, "specific_stock.html", context={
        "ticker": ticker,
        "price": stock_price,
        "top_pos": top_tweets_pos,
        "top_neg": top_tweets_neg,
        "top_sentiment": top_tweets_sentiment,
        "latest_pos": latest_tweets_pos,
        "latest_neg": latest_tweets_neg,
        "latest_sentiment": latest_tweets_sentiment,
    })
