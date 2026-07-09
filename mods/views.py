from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Asset, Game  
from .forms import AssetForm, GameForm

def home_page(request):
    game_id = request.GET.get('game')
    
    if game_id:
        assets = Asset.objects.filter(game_id=game_id).select_related('game', 'author')
    else:
        assets = Asset.objects.all().select_related('game', 'author')
        
    games = Game.objects.all()
    
    return render(request, 'mods/index.html', {
        'assets': assets,
        'games': games,
        'current_game': int(game_id) if game_id and game_id.isdigit() else None,
        'total_assets_count': Asset.objects.count()
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте введённые данные.")
    else:
        form = UserCreationForm()
    return render(request, 'mods/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'mods/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def create_asset_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.author = request.user  
            asset.save()
            return redirect('home')
    else:
        form = AssetForm()
    return render(request, 'mods/create_asset.html', {'form': form})

def create_game_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'mods/create_game.html', {'form': form})
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def download_asset_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    
    if asset.file:
        asset.downloads_count += 1
        asset.save(update_fields=['downloads_count']) 
        
        return HttpResponseRedirect(asset.file.url)
        
    messages.error(request, "Файл для этой модификации отсутствует.")
    return redirect('home')