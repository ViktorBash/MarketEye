from django.urls import path
from stocks import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:ticker>/', views.stock_ticker, name="ticker"),
    path('test/convert_data/', views.convert_data, name="thedata")
]