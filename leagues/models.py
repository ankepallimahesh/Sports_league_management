from django.db import models
from accounts.models import Team

class League(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teams = models.ManyToManyField(Team, blank=True, related_name='leagues')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='seasons')
    year = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.league.name} {self.year}"
