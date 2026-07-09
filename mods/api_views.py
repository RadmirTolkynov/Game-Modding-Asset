from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# Строго относительные импорты модулей из текущей папки
from .models import Game, Asset
from .serializers import GameSerializer, AssetSerializer

# === 1. API для Игр (Функции / FBV) ===

@api_view(['GET', 'POST'])
# IsAuthenticatedOrReadOnly: GET доступен всем, POST — только по Токену/Сессии
@permission_classes([IsAuthenticatedOrReadOnly])
def game_list_api(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = GameSerializer(data=request.POST) # или request.data для JSON
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def game_detail_api(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response({'error': 'Игра не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# === 2. API для Модов/Ассетов (Классы / CBV) ===

class AssetListAPIView(APIView):
    # Указываем типы аутентификации (по токену в заголовке или по сессии в браузере)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        assets = Asset.objects.all().select_related('game', 'author')
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            # Автоматически привязываем автора мода к текущему вошедшему пользователю
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            return None

    def get(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response({'error': 'Ассет не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    def put(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response({'error': 'Ассет не найден'}, status=status.HTTP_404_NOT_FOUND)
            
        # Защита: редактировать мод может только его автор или суперюзер
        if asset.author != request.user and not request.user.is_staff:
            return Response({'error': 'У вас нет прав на редактирование этого мода'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response({'error': 'Ассет не найден'}, status=status.HTTP_404_NOT_FOUND)
            
        if asset.author != request.user and not request.user.is_staff:
            return Response({'error': 'У вас нет прав на удаление этого мода'}, status=status.HTTP_403_FORBIDDEN)
            
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)