from django.db import models
from accounts.models import Team

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BracketMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='bracket_matches')
    round_number = models.PositiveIntegerField()
    home = models.ForeignKey(Team, related_name='br_home', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='br_away', on_delete=models.CASCADE)
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    played = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tournament.name} R{self.round_number}: {self.home} vs {self.away}"

    def winner(self):
        if not self.played: 
            return None
        return self.home if (self.home_score or 0) > (self.away_score or 0) else self.away
