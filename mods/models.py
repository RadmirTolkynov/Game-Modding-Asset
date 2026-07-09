from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=100)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.title

class Asset(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    version = models.CharField(max_length=20, default='1.0.0')
    file = models.FileField(upload_to='mods_files/', null=True, blank=True)
    downloads_count = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='assets')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')

    def __str__(self):
        return self.title

class Review(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} on {self.asset.title}"