from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from . import api_views
urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('asset/new/', views.create_asset_view, name='create_asset'),
    path('game/new/', views.create_game_view, name='create_game'),

    path('api/games/', api_views.game_list_api, name='game_list_api'),
    path('api/games/<int:pk>/', api_views.game_detail_api, name='game_detail_api'),
    path('api/assets/', api_views.AssetListAPIView.as_view(), name='asset_list_api'),
    path('api/assets/<int:pk>/', api_views.AssetDetailAPIView.as_view(), name='asset_detail_api'),
    
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('asset/<int:pk>/download/', views.download_asset_view, name='download_asset'),
]