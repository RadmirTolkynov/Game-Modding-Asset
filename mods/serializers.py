from rest_framework import serializers
from .models import Game, Asset, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False)

class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance



class ReviewSerializer(serializers.ModelSerializer):
    author_details = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'text', 'created_at', 'asset', 'author', 'author_details']
        read_only_fields = ['author']

class AssetSerializer(serializers.ModelSerializer):
    game_details = GameSerializer(source='game', read_only=True)
    author_details = UserSerializer(source='author', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)  
    class Meta:
        model = Asset
        fields = ['id', 'title', 'description', 'version', 'downloads_count', 'game', 'author', 'game_details', 'author_details', 'reviews']  # Добавили 'reviews' в конец!
        read_only_fields = ['author', 'downloads_count']