from rest_framework import serializers
from main import models
from accounts import models as accountModels
from django.contrib.auth import authenticate
class NewsSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    class Meta:
        model = models.News
        fields = "__all__"
        #fields = ["title", "description", "url", "published_date", "publisher", "asset_ticker"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetCategory
        fields = "__all__"
        #fields = ["category_name", "slug"]

class AssetSerializer(serializers.ModelSerializer):
    asset_category_name = serializers.CharField(source='asset_category.category_name')
    class Meta:
        model = models.Asset
        fields = "__all__"
        # fields = ["asset_name",	"asset_ticker", "last_price", "asset_category_name", "view_count", "photo_link", "market_size","favourite_count"]

class CommentSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.Comment
        fields = "__all__"
        #fields = ["username", "asset_ticker", "comment_text", "date_time", "parent_comment", "like_count", "imported_from"]

class FavouriteAssetSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.FavouriteAsset
        fields = "__all__"
        #fields = ["username", "asset_ticker", "favourite_date"]

class FavouriteCategorySerializer(serializers.ModelSerializer):
    asset_category_name = serializers.CharField(source='asset_category.category_name')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.FavouriteCategory
        fields = "__all__"
        #fields = ["username", "asset_category_name", "favourite_date"]

"""
class CommentLikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='liked_users.username')
    class Meta:
        model = models.Comment
        fields = "__all__"
        #fields = ["id","date_time" "username"]
"""

class AssetPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetPrice
        fields = "__all__"

class AllAssetPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = "__all__"
        #fields = ["asset_name", "asset_ticker", "last_price"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountModels.CustomUser
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = accountModels.CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
