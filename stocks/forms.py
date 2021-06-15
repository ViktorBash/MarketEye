from django import forms


class StockSearchForm(forms.Form):
    ticker = forms.CharField(label="", max_length=5, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder' : 'Example: TSLA'}))
