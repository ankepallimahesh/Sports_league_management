# tournaments/forms.py
from django import forms
from .models import Tournament
from accounts.models import Team

class TournamentForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 8})
    )

    class Meta:
        model = Tournament
        fields = ['name', 'teams']
