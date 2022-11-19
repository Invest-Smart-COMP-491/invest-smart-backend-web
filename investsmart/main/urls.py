"""investsmart_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
	path("",views.HomeView.as_view(),name="homepage"),
    path("category",views.HomeView.as_view(),name="homepage"), # for now 
    path("updateAssets",views.updateAssetsView.as_view(),name="updateAssets"),
    path("updateNews",views.updateNewsView.as_view(),name="updateNews"),
    path("updatePrices",views.updatePricesView.as_view(),name="updatePrices"),
    path("<slug:slug>", views.categoryView.as_view(), name="category_detail"),
    path("asset/<slug:slug>", views.AssetDetailView.as_view(), name="asset_detail"),
    path("asset/", views.AssetDetailView.as_view(), name="assets"),
    path("asset/<slug:slug>/price", views.AssetPriceView.as_view(), name="asset_price"),
    path("asset/price", views.AssetPriceView.as_view(), name="price"),
    path("asset/<slug:slug>/news", views.AssetNewsView.as_view(), name="asset_news"),
    path("asset/news", views.AssetNewsView.as_view(), name="news"),
    path("asset/fav", views.CurrentUserFavouriteAssetsView.as_view(), name="favourite_assets"),
    path("asset/favCategory", views.CurrentUserFavouriteCategoryView.as_view(), name="favourite_categories"),
]
