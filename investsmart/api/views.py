from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main.models import Asset, News
from .serializers import APISerializer

class NewsApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #news = News.objects.filter(user=request.asset_ticker)
        if len(kwargs) > 0:
            print(kwargs)
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in Asset.objects.all()]
            if slug in assets:
                asset = Asset.objects.filter(asset_ticker=slug).first()
                news = News.objects.filter(asset=asset)
        else:
            news = News.objects.all()
        
        serializer = APISerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    """def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

class PriceApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #news = News.objects.filter(user=request.asset_ticker)
        if len(kwargs) > 0:
            print(kwargs)
            slug = kwargs.get('slug')
            assets = [c.asset_ticker for c in Asset.objects.all()]
            if slug in assets:
                ret = Asset.objects.all().last_price.filter(asset_ticker=slug).first()
        else:
            ret = Asset.objects.all().last_price
        
        serializer = APISerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)