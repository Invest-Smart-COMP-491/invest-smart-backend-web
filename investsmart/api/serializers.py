from rest_framework import serializers
from main import models

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = ["title", "description", "url", "published_date", "publisher", "asset"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetCategory
        fields = ["category_name", "slug"]

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = ["asset_name",	"asset_ticker", "last_price", "asset_category", "view_count", "photo_link", "market_size"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["user", "asset", "comment_text", "date_time", "parent_comment", "like_count", "imported_from"]

class FavouriteAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavouriteAsset
        fields = ["user", "asset", "favourite_date"]

class FavouriteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavouriteCategory
        fields = ["user", "asset_category", "favourite_date"]

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = ["comment", "user"]

class AssetPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetPrice
        fields = ["asset", "date_time","price","volume"]