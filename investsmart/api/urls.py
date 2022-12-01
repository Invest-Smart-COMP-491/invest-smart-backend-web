from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('news/', views.NewsApiView.as_view()),
    path("news/<slug:slug>", views.NewsApiView.as_view(), name="asset_news"),
    path("prices/", views.PriceApiView.as_view()),
    path("prices/<slug:slug>", views.PriceApiView.as_view(), name="asset_news"),
    path("categories/", views.CategoryApiView.as_view()),
    path("assets/", views.AssetsApiView.as_view()),
    path("assets/<slug:slug>", views.AssetsApiView.as_view()),
    path("comments/", views.CommentsApiView.as_view()),
    path("trending-stocks/", views.TrendingStocksApiView.as_view()),
    path("comments/<slug:slug>", views.CommentsApiView.as_view(), name="asset_comments"),
#    path("commentLikes/", views.CommentsLikesApiView.as_view()),
#    path("commentLikes/<slug:slug>", views.CommentsLikesApiView.as_view(), name="comments_likes"),
    path("assets/fav", views.CurrentUserFavouriteAssetsApiView.as_view(), name="favourite_assets"),
    path("assets/favCategory", views.CurrentUserFavouriteCategoryApiView.as_view(), name="favourite_categories"),
]