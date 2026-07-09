from django import forms
from .models import Asset, Game

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['title', 'description', 'version', 'game', 'file']
        labels = {
            'title': 'Название мода:',
            'description': 'Описание:',
            'version': 'Версия:',
            'game': 'Игра:',
            'file': 'Файл модификации (архив):',
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title']  
        labels = {
            'title': 'Название игры',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например, Arena Breakout или The Battle Cats',
                'style': 'width: 100%; padding: 10px; background: #222227; border: 1px solid #2a2a30; border-radius: 6px; color: white;'
            }),
        }