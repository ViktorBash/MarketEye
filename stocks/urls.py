from django.urls import path
from stocks import views

urlpatterns = [
    path('', views.home, name="home"),
]