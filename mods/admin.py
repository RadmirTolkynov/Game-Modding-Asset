from django.contrib import admin
from .models import Game, Asset, Review

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'author', 'version', 'downloads_count')
    list_filter = ('game',)
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('asset', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text',)