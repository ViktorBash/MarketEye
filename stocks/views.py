from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockSearchForm
from .webscraper import TwitterAPI
from .stock_information import get_latest_stock_price
from .machine_learning import get_sentiment, clean_string
import os
import csv


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
    with open("stocks/data/spy_list.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if line['Symbol'] == ticker:
                pass_check_1 = True
    csv_file.close()

    if not pass_check_1:
        return redirect("home")

    # All checks are passed by this point 🚀 🚀 🚀
    print("check 1")

    stock = Stock.objects.get_or_create(ticker=ticker)

    # Get a list of tweets that mention the stock
    twitter_api_instance = TwitterAPI(ticker, os.environ.get("BEARER_TOKEN"), 5)  # Bearer token = Twitter API Key
    twitter_api_instance.start_scraping()
    text_array = twitter_api_instance.text_list

    # Clean all the strings in the array
    for i in range(len(text_array)):
        text_array[i] = clean_string(text_array[i])

    print("check 2")

    # Number of pos/neg tweets
    total_negative = 0
    total_positive = 0

    # Creating a list that holds all of the analysis, array is filled with Sentence classes
    sentiment_array = []
    for i in range(len(text_array)):
        sentiment = get_sentiment(text_array[i])
        if sentiment.labels[0].value == "POSITIVE":
            total_positive += 1
        else:
            total_negative += 1
        sentiment_array.append(sentiment)

    print("check 3")
    # TODO: Redo writing to CSV

    # # Create/Write over a CSV file
    # with open(f"stocks/stock_name_csv/{ticker}.csv", "w", newline="", encoding="utf-8") as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     for item in array:
    #         sentiment_model = get_sentiment(item)
    #         csv_writer.writerow([item, sentiment_model.labels[0].value, sentiment_model.labels[0].score])
    #         total += sentiment_model.labels[0].score
    #         counter += 1
    # csv_file.close()

    emotion = "positive"
    if total_negative > total_positive:
        emotion = "negative"
    elif total_negative == total_positive:
        emotion = "neutral"

    print("check 4")

    stock_price = get_latest_stock_price(ticker)

    return render(request, "specific_stock.html", context={
        "ticker": ticker,
        "price": stock_price,
        "sentiment": emotion,
    })
