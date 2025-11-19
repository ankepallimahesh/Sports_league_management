# matches/forms.py
from django import forms
from django.utils import timezone
from .models import Match, Goal
from accounts.models import Team, Player

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_score', 'away_score', 'played']
        widgets = {
            'home_score': forms.NumberInput(attrs={'min': 0}),
            'away_score': forms.NumberInput(attrs={'min': 0}),
        }

class MatchCreateForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['league', 'date', 'home', 'away', 'home_score', 'away_score', 'played']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned = super().clean()
        home = cleaned.get('home')
        away = cleaned.get('away')
        date = cleaned.get('date')
        if home and away and home == away:
            raise forms.ValidationError("Home and away teams must be different.")
        # Prevent creating matches in the past
        if date:
            now = timezone.now()
            # If user's datetime-local input produced a naive datetime, compare using aware now
            if date < now:
                self.add_error('date', 'Match date cannot be in the past.')
        return cleaned

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['player', 'minute']
    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)
        super().__init__(*args, **kwargs)
        if match:
            players_qs = match.home.players.all() | match.away.players.all()
            self.fields['player'].queryset = players_qs.distinct()
