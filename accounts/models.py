from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='players/', null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name or self.user.get_username() if self.user else 'Player'

class Team(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='teams/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(Player, blank=True, related_name='teams')

    def __str__(self):
        return self.name
