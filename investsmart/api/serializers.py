from rest_framework import serializers

from main.models import News

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["title", "description", "url", "published_date", "publisher", "asset"]