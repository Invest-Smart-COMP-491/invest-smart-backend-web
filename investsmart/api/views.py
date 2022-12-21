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
from rest_framework import generics
from rest_framework import filters
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer



class NewsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
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


class UserFavouriteAssetsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):

        # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()
        request.data
        request.user
        favouriteAssets = models.FavouriteAsset.objects.filter(user=user) # list 

        if len(kwargs) > 0:

            asset_ticker = kwargs.get('slug')
            favouriteAssets = models.FavouriteAsset.objects.filter(asset__asset_ticker=asset_ticker) # list
            users = [c.user for c in favouriteAssets]

            
            serializer = serializers.UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) # return users who liked given asset 
        
        serializer = serializers.FavouriteAssetSerializer(favouriteAssets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # returns current user's liked assets
    
    def post(self,request,*args, **kwargs):

        if len(kwargs) > 0: # asset_ticker as slug 

            asset = models.Asset.objects.filter(asset_ticker = kwargs.get('slug')).first()
            # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
            user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()

            favAsset = models.FavouriteAsset(asset=asset,user=user)
            favAsset.save()

            serializer= serializers.FavouriteAssetSerializer(data=favAsset)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()

        if len(kwargs) > 0:
            #print(kwargs)
            asset_ticker = kwargs.get('slug')
            favouriteAsset = models.FavouriteAsset.objects.filter(asset__asset_ticker=asset_ticker,user=user).first()
            favouriteAsset.delete()
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserFavouriteAssetNewsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):

        # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()
        request.data
        request.user
        favouriteAssets = models.FavouriteAsset.objects.filter(user=user).values_list('asset__asset_ticker', flat=True) # list 
        favouriteNews = models.News.objects.filter(asset__asset_ticker__in = favouriteAssets)
        
        serializer = serializers.NewsSerializer(favouriteNews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # returns current user's liked asset news 



class UserFavouriteCategoryApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):

        # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()
        favouriteCategories = models.FavouriteCategory.objects.filter(user=user) # list 

        if len(kwargs) > 0:

            
            slug = kwargs.get('slug')
            favouriteCategories = models.FavouriteCategory.objects.filter(asset_category__slug=slug) # list
            users = [c.user for c in favouriteCategories]

            
            serializer = serializers.UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) # return users who liked given categories 
        
        serializer = serializers.FavouriteCategorySerializer(favouriteCategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # returns current user's liked categories
    
    def post(self,request,*args, **kwargs):

        if len(kwargs) > 0: # slug as slug 

            asset_category = models.AssetCategory.objects.filter(slug=kwargs.get('slug')).first()
            # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
            user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()

            favCat = models.FavouriteCategory(asset_category__slug=asset_category,user=user)
            favCat.save()

            serializer= serializers.FavouriteCategorySerializer(data=favCat)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, *args, **kwargs):

        # user = self.context.get("request").user # we need to decide on this : should we send username or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()

        if len(kwargs) > 0:
            #print(kwargs)
            slug = kwargs.get('slug')
            favouriteCategory = models.FavouriteCategory.objects.filter(asset_category__slug=slug,user=user).first()
            favouriteCategory.delete()
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PriceApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):

        serializer = None

        if len(kwargs) > 0:
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
    permission_classes = (permissions.AllowAny,)
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


class AssetsApiView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    search_fields = ['asset_name', 'asset_ticker']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializer

    def get(self, request, *args, **kwargs):
        
        if len(kwargs) > 0:
            slug = kwargs.get('slug') 
            assets = [c.asset_ticker for c in models.Asset.objects.all()]

            if slug in assets: # if slug is asset_ticker
                assets = models.Asset.objects.filter(asset_ticker=slug).first()
                serializer = serializers.AssetSerializer(assets, many=False)

            else: # if slug is asset category, return asset array
                assets = models.Asset.objects.filter(asset_category__slug=slug)
                serializer = serializers.AssetSerializer(assets, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)


        else:
            return self.list(request, *args, **kwargs)
    
    def post(self,request):

        serializer= serializers.AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        if len(kwargs) > 0:
            ticker = kwargs.get('slug')
            asset = models.Asset.objects.filter(asset_ticker=ticker).first()
            comments = models.Comment.objects.filter(asset=asset)
            if 'parent_comment' in request.query_params:
                parent_comment_id = request.query_params["parent_comment"]
                if parent_comment_id == '':
                    comments = comments.filter(parent_comment=None)
                else:
                    parent_comment = models.Comment.objects.filter(id=parent_comment_id).first()
                    comments = comments.filter(parent_comment=parent_comment)
            serializer = serializers.CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        # return Response(status=status.HTTP_400_BAD_REQUEST) # TODO: replace below ones with this one 

        comments = models.Comment.objects.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        
        
    def post(self, request):
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            try:
                user = authToken.user
                asset = models.Asset.objects.filter(asset_ticker=request.data["asset_ticker"]).first()
                text = request.data["comment_text"]
                parent_comment = None
                if "parent_comment_id" in request.data:
                    parent_comment_id = request.data["parent_comment_id"]
                    parent_comment=models.Comment.objects.filter(id=parent_comment_id).first()
                created_comment = models.Comment(user=user, asset=asset, comment_text=text, parent_comment=parent_comment)
                created_comment.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self,request, *args, **kwargs):
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            try:
                user = authToken.user
                id = request.data["id"]
                text = request.data["comment_text"]
                comment = models.Comment.objects.filter(id=id, user=user).first()
                comment.comment_text = text
                comment.save()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            try:
                user = authToken.user
                id = request.data["id"]
                comment = models.Comment.objects.filter(id=id, user=user).first()
                comment.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TrendingStocksApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        top_n = 10 # top 10 news, can be reassigned 
		
		#asset_ls = getPopularAssets()
		#top_assets = models.Asset.objects.filter(asset_ticker__in = asset_ls)[:top_n]
        top_assets = models.Asset.objects.all().order_by("-popularity")[:top_n]

        serializer = serializers.AssetSerializer(top_assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass

class TrendingStockNewsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):

        top_n = 10 # top 10 assets, can be reassigned 
		
        top_assets = models.Asset.objects.all().order_by("-popularity")[:top_n].values_list('asset_ticker', flat=True) # list 
        favouriteNews = models.News.objects.filter(asset__asset_ticker__in = top_assets)
        
        serializer = serializers.NewsSerializer(favouriteNews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # returns current user's liked asset news 


class UserApiView(APIView):
    """Returns the user information that is associated with the username passed as slug.
    Might be good idea to fetch all user comments and favorites as well."""
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        ret = models.CustomUser.objects.filter(username=slug)

        serializer = serializers.UserSerializer(ret, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass

"""
class CommentsLikesApiView(APIView):
    permission_classes = (permissions.AllowAny,)
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

class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data["user"] = serializers.UserSerializer(user, many=False).data
        return Response(temp_list.data)


class FavouriteAssetsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        favouriteAssets = models.FavouriteAsset.objects.none()
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            if authToken is not None:
                favouriteAssets = models.FavouriteAsset.objects.filter(user=authToken.user).all()
            
            if len(favouriteAssets) > 0:
                favouriteAssets = [f.asset for f in favouriteAssets]

            serializer = serializers.AssetSerializer(favouriteAssets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.FavouriteAssetSerializer(None)
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            if authToken is not None:
                user = authToken.user
                if 'asset' in request.query_params:
                    asset_ticker = request.query_params['asset']
                    asset = models.Asset.objects.filter(asset_ticker = asset_ticker).first()
                if user is not None and asset is not None:
                    try:
                        favAsset = models.FavouriteAsset(asset=asset,user=user)
                        favAsset.save()
                        serializer = serializers.FavouriteAssetSerializer(favAsset)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        favAsset = models.FavouriteAsset.objects.filter(asset=asset,user=user).first()
                        serializer = serializers.FavouriteAssetSerializer(favAsset)
                        return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            if authToken is not None:
                user = authToken.user
                if 'asset' in request.query_params:
                    asset_ticker = request.query_params['asset']
                    asset = models.Asset.objects.filter(asset_ticker = asset_ticker).first()
                if user is not None and asset is not None:
                    try:
                        favAsset = models.FavouriteAsset.objects.filter(asset=asset, user=user).first()
                        favAsset.delete()
                        return Response(status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class FavouriteAssetsNewsApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        favouriteAssets = models.FavouriteAsset.objects.none()
        favouriteNews = models.News.objects.none()
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization'].split(" ")[1][:8]
            authToken = AuthToken.objects.filter(token_key=token).first()
            if authToken is not None:
                favouriteAssets = models.FavouriteAsset.objects.filter(user=authToken.user).values_list('asset__asset_ticker', flat=True)
            
            if len(favouriteAssets) > 0:
                favouriteNews = models.News.objects.filter(asset__asset_ticker__in = favouriteAssets)

            serializer = serializers.NewsSerializer(favouriteNews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)