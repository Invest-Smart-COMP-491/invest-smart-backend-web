import numpy as np
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main import models,helper
from . import serializers
from accounts import models as accountModels
from reco.stock_recommender import SimilarStocks, getPopularAssets



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
            """sse = SimilarStocks()
            sse.buildSimilarityDict()"""

            news = models.News.objects.all()
        
        serializer = serializers.NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):

        serializer= serializers.NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserFavouriteAssetsApiView(APIView):
    def get(self, request, *args, **kwargs):

        user = request.user
        ret = models.FavouriteAsset.objects.filter(user=user)
        # ret = np.array([])
        
        serializer = serializers.FavouriteAssetSerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):

        serializer= serializers.FavouriteAssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserFavouriteCategoryApiView(APIView):
    def get(self, request, *args, **kwargs):

        user = request.user
        ret = models.FavouriteCategory.objects.filter(user=user)
        
        serializer = serializers.FavouriteCategorySerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):

        serializer= serializers.FavouriteCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriceApiView(APIView): 
    def get(self, request, *args, **kwargs):

        serializer = None
        assetPrices = None # TODO: handle if no assetPrices 

        if len(kwargs) > 0:
            # TODO: slug can be category slug or asset_ticker handle it. 
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
    
    def post(self,request):

        serializer= serializers.AssetPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        categories = models.AssetCategory.objects.all()
        
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):

        serializer= serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetsApiView(APIView):
    def get(self, request, *args, **kwargs):

        if len(kwargs) > 0:
            #print(kwargs)
            slug = kwargs.get('slug') 
            assets = [c.asset_ticker for c in models.Asset.objects.all()]
            if slug in assets: # if slug is asset_ticker
                assets = models.Asset.objects.filter(asset_ticker=slug).first()
            else: # if slug is asset category, return asset array
                assets = models.Asset.objects.filter(asset_category__slug=slug)


        else:
            assets = models.Asset.objects.all()
        
        serializer = serializers.AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):

        serializer= serializers.AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self,request):

        serializer= serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrendingStocksApiView(APIView):
    def get(self, request, *args, **kwargs):
        asset_ls = getPopularAssets()
        ret = models.Asset.objects.filter(asset_ticker__in = asset_ls)

        serializer = serializers.AssetSerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass
"""
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
"""