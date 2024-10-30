from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from favorite.models import Favorite


class FavoriteListCreateAPISerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        # depth = 1

    def validate(self, attrs):
        queryset = Favorite.objects.filter(post=attrs["post"], user=attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("Bu post favorilerinize zaten eklendi!...")
        return attrs


class FavoriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('content', 'post', 'user')
