# matches/models.py
from django.db import models
from leagues.models import League
from accounts.models import Team, Player

class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    date = models.DateTimeField(null=True, blank=True)
    home = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.PositiveIntegerField(null=True, blank=True, default=0)
    away_score = models.PositiveIntegerField(null=True, blank=True, default=0)
    played = models.BooleanField(default=False)

    class Meta:
        unique_together = ('home', 'away', 'date')

    def __str__(self):
        return f"{self.home} vs {self.away} ({self.date})"

    def winner(self):
        if not self.played:
            return None
        if (self.home_score or 0) > (self.away_score or 0):
            return self.home
        elif (self.away_score or 0) > (self.home_score or 0):
            return self.away
        return None

    def goals(self):
        """Return queryset of Goal objects for this match."""
        return self.goal_set.all()

    def goals_for_team(self, team):
        return self.goal_set.filter(player__teams=team).count()

class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.full_name} goal in {self.match} @ {self.minute}'"
