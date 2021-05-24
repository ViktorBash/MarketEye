from django import forms


class StockSearchForm(forms.Form):
    ticker = forms.CharField(label="", max_length=5)
