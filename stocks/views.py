from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockSearchForm


# Create your views here.
def home(request):
    print("E")
    if request.method == "POST":
        print("e")
        form = StockSearchForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            return redirect("ticker", ticker=ticker)
    else:
        form = StockSearchForm()
    return render(request, "home.html", {"form": form})


def stock_sticker(request, ticker):
    print(ticker)
    return render(request, "specific_stock.html", context={
        "ticker": ticker,
    })
