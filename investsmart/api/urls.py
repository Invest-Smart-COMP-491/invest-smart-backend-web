from django.contrib import admin
from django.urls import path, include

from .views import (
    NewsApiView,
    #PriceApiView,
)

urlpatterns = [
    path('news/', NewsApiView.as_view()),
    path("news/<slug:slug>", NewsApiView.as_view(), name="asset_news"),
    #path("prices/", PriceApiView.as_view()"),
    #path("prices/<slug:slug>", PriceApiView.as_view(), name="asset_news"),
]