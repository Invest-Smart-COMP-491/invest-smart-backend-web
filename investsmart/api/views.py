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


class UserFavouriteAssetsApiView(APIView):
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



class UserFavouriteCategoryApiView(APIView):
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

            serializer = serializers.CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        # return Response(status=status.HTTP_400_BAD_REQUEST) # TODO: replace below ones with this one 

        comments = models.Comment.objects.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        
        
    def post(self,request):
        
        # user_id, asset_ticker , comment_text, (optional) parent_comment

        # user = self.context.get("request").user # we need to decide on this : should we send user_id or django helps with this method? 
        user = accountModels.CustomUser.objects.filter(username=request.data["username"]).first()
        asset = models.Asset.objects.filter(asset_ticker=request.data["asset_ticker"]).first()
        parent_comment = None
        if "parent_comment_id" in request.data:
            parent_comment_id = request.data["parent_comment_id"]
            parent_comment=models.Comment.objects.filter(id=parent_comment_id).first()
        
        created_comment = models.Comment(user=user,asset=asset,comment_text=request.data["comment_text"],parent_comment=parent_comment)
        created_comment.save()

        return Response(status=status.HTTP_201_CREATED)
        
        #TODO: there is problem with serializer?
        # serializer= serializers.CommentSerializer(data=created_comment)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request, *args, **kwargs):

        id=request.data["id"]
        comment = models.Comment.objects.filter(id=id).first()
        comment.comment_text = request.data["comment_text"]
        comment.save()
        # serializer= serializers.CommentSerializer(data=comment)
        return Response(status=status.HTTP_200_OK)

        """
        if len(kwargs) > 0:
            #print(kwargs)
            id = kwargs.get('slug')
            comment = models.Comment.objects.filter(id=id)
            comment.comment_text=request.data["comment_text"]
            comment.save()
            serializer= serializers.CommentSerializer(data=comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)"""
    
    def delete(self, request, *args, **kwargs):

        id=request.data["id"]
        comment = models.Comment.objects.filter(id=id).first()
        comment.delete()
    
        return Response(status=status.HTTP_200_OK)
        """
        if len(kwargs) > 0:
            #print(kwargs)
            id = kwargs.get('slug')
            comment = models.Comment.objects.filter(id=id).first()
            comment.delete()
        
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
        """


class TrendingStocksApiView(APIView):
    def get(self, request, *args, **kwargs):
        top_n = 10 # top 10 news, can be reassigned 
		
		#asset_ls = getPopularAssets()
		#top_assets = models.Asset.objects.filter(asset_ticker__in = asset_ls)[:top_n]
        top_assets = models.Asset.objects.all().order_by("-popularity")[:top_n]

        serializer = serializers.AssetSerializer(top_assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass

class UserApiView(APIView):
    """Returns the user information that is associated with the username passed as slug.
    Might be good idea to fetch all user comments and favorites as well."""
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        ret = models.CustomUser.objects.filter(username=slug)

        serializer = serializers.UserSerializer(ret, many=True)
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