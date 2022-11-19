from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main import models
from accounts import models as accountModels
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
                asset = models.Asset.objects.filter(asset_ticker=slug).first()
                assetPrices = models.AssetPrice.objects.filter(asset=asset)
                serializer = serializers.AssetPriceSerializer(assetPrices, many=True)

        else:
            #TODO: do not return all prices only last prices is enough 
            #assetPrices = models.AssetPrice.objects.order_by("-date_time").distinct("asset__asset_ticker").all() # distinct not supported in sqlite3 - can be used for postgre 

            # for now - get number of assets(n) and get ordered n entry 
            #p = models.Asset.objects.count()
            #assetPrices = models.AssetPrice.objects.order_by("-date_time","asset__asset_ticker").all()[:p]

            print("--------------------")
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
