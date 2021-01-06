from rest_framework import serializers
from .models import User, Favourites


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'favourites', 'email')


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = "__all__"
