from django.contrib.auth import login
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main import models
from main import helper
from accounts import models as accountModels
from main.models import CommentLike
from . import serializers

import numpy as np

class NewsApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            #print(kwargs)
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in models.Asset.objects.all()]
            if slug in assets:
                asset = models.Asset.objects.filter(asset_ticker=slug).first()
                news = models.News.objects.filter(asset=asset)
        else:
            news = models.News.objects.all()
        
        serializer = serializers.NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentUserFavouriteAssetsApiView(APIView):
    def get(self, request, *args, **kwargs):

        user = request.user
        ret = models.FavouriteAsset.objects.filter(user=user)
        # ret = np.array([])
        
        serializer = serializers.FavouriteAssetSerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentUserFavouriteCategoryApiView(APIView):
    def get(self, request, *args, **kwargs):

        user = request.user
        ret = models.FavouriteCategory.objects.filter(user=user)
        
        serializer = serializers.FavouriteCategorySerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PriceApiView(APIView): 
    def get(self, request, *args, **kwargs):

        serializer = None
        assetPrices = None # TODO: handle if no assetPrices 

        if len(kwargs) > 0:
            #print(kwargs) 
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in models.Asset.objects.all()]
            if slug in assets:
                #asset = models.Asset.objects.filter(asset_ticker=slug).first()
                #assetPrices = models.AssetPrice.objects.filter(asset=asset)
                assetPrices = helper.getAssetPrice(slug)  # do not save to the database directly gets from api 
                serializer = serializers.AssetPriceSerializer(assetPrices, many=True)
        else:
            assets = models.Asset.objects.all()
            serializer = serializers.AllAssetPriceSerializer(assets, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        categories = models.AssetCategory.objects.all()
        
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssetsApiView(APIView):
    def get(self, request, *args, **kwargs):

        if len(kwargs) > 0:
            #print(kwargs)
            # category_id = kwargs.get('category_id') # category_id also can be used 
            slug = kwargs.get('slug') 
            assets = models.Asset.objects.filter(asset_category__slug=slug)

        else:
            assets = models.Asset.objects.all()
        
        serializer = serializers.AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentsApiView(APIView):
    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            #print(kwargs)
            ticker = kwargs.get('slug')
            asset = models.Asset.objects.filter(asset_ticker=ticker).first()
            comments = models.Comment.objects.filter(asset=asset)
        else:
            comments = models.Comment.objects.all()
        
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsLikesApiView(APIView):
    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            #print(kwargs)
            comment_id = kwargs.get('slug')
            commentlikes = CommentLike.objects.get(comment_id=comment_id)
        else:
            #commentlikes = models.CommentLike.objects.all() # TODO: do not return all comment, maybe something else can be applied 
            commentslikes = np.array([])
        
        serializer = serializers.CommentLikeSerializer(commentslikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from . import serializers

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)