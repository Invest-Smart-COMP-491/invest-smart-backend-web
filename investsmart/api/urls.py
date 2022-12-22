from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from .views import LoginAPI

from . import views

urlpatterns = [
    path('news/', views.NewsApiView.as_view()),
    path("news/<slug:slug>", views.NewsApiView.as_view(), name="asset_news"),
    path("prices/", views.PriceApiView.as_view()),
    path("prices/<slug:slug>", views.PriceApiView.as_view(), name="asset_prices"),
    path("categories/", views.CategoryApiView.as_view()),
    path("assets/", views.AssetsApiView.as_view()),
    path("assets", views.AssetsApiView.as_view()),
    path("assets/<slug:slug>", views.AssetsApiView.as_view()),
    path("trending-stocks/", views.TrendingStocksApiView.as_view()),
    path("trending-stocks/news/", views.TrendingStockNewsApiView.as_view()),
    path("comments", views.CommentsApiView.as_view()),
    path("comments/", views.CommentsApiView.as_view(), name="asset_comments"),
#    path("commentLikes/", views.CommentsLikesApiView.as_view()),
#    path("commentLikes/<slug:slug>", views.CommentsLikesApiView.as_view(), name="comments_likes"),
    path("assets/fav/<slug:slug>", views.UserFavouriteAssetsApiView.as_view(), name="favourite_assets"),
    path("assets/fav/news/", views.UserFavouriteAssetNewsApiView.as_view(), name="favourite_asset_news"),
    path("assets/favCategory/<slug:slug>", views.UserFavouriteCategoryApiView.as_view(), name="favourite_categories"),
    path("users/", views.UserApiView.as_view(), name="users"),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path("favourite", views.FavouriteAssetsApiView.as_view(), name="favourite_assets"),
    path("favourite/", views.FavouriteAssetsApiView.as_view(), name="favourite_assets"),
    path("favourite/news/", views.FavouriteAssetsNewsApiView.as_view(), name="favourite_assets"),  
    path("recommend/", views.RecommendAssetsApiView.as_view(), name="recommend_assets"),  
]