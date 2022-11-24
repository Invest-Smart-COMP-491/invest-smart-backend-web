from rest_framework import serializers
from main import models

class NewsSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    class Meta:
        model = models.News
        fields = ["title", "description", "url", "published_date", "publisher", "asset_ticker"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetCategory
        fields = ["category_name", "slug"]

class AssetSerializer(serializers.ModelSerializer):
    asset_category_name = serializers.CharField(source='asset_category.category_name')
    class Meta:
        model = models.Asset
        fields = ["asset_name",	"asset_ticker", "last_price", "asset_category_name", "view_count", "photo_link", "market_size"]

class CommentSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.Comment
        fields = ["username", "asset_ticker", "comment_text", "date_time", "parent_comment", "like_count", "imported_from"]

class FavouriteAssetSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.FavouriteAsset
        fields = ["username", "asset_ticker", "favourite_date"]

class FavouriteCategorySerializer(serializers.ModelSerializer):
    asset_category_name = serializers.CharField(source='asset_category.category_name')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.FavouriteCategory
        fields = ["username", "asset_category_name", "favourite_date"]

class CommentLikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = models.CommentLike
        fields = ["comment", "username"]

class AssetPriceSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.asset_name')
    asset_ticker = serializers.CharField(source='asset.asset_ticker')
    class Meta:
        model = models.AssetPrice
        fields = ["asset_name","asset_ticker", "date_time","price","volume"]

class AllAssetPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = ["asset_name", "asset_ticker", "last_price"]

#TODO: Refactor
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs