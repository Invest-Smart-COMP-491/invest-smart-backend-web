from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main import models
from . import serializers

class NewsApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            print(kwargs)
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in models.Asset.objects.all()]
            if slug in assets:
                asset = models.Asset.objects.filter(asset_ticker=slug).first()
                news = models.News.objects.filter(asset=asset)
        else:
            news = models.News.objects.all()
        
        serializer = serializers.NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PriceApiView(APIView):
    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            print(kwargs)
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in models.Asset.objects.all()]
            if slug in assets:
                ret = models.Asset.objects.all().last_price.filter(asset_ticker=slug).first()
        else:
            ret = models.Asset.objects.all().last_price
        
        serializer = serializers.NewsSerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        categories = models.AssetCategory.objects.all()
        
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssetApiView(APIView):
    def get(self, request, *args, **kwargs):
        assets = models.Asset.objects.all()
        
        serializer = serializers.AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsApiView(APIView):
    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            print(kwargs)
            slug = kwargs.get('slug')
            asset = models.Asset.objects.filter(asset_ticker=slug).first()
            #TODO: Is asset_id check correct?
            comments = models.Comment.objects.filter(asset_id=asset)
        else:
            comments = models.Comment.objects.all()
        
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
