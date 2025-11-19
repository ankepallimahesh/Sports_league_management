# leagues/forms.py
from django import forms
from .models import League
from accounts.models import Team

class LeagueForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 6})
    )

    class Meta:
        model = League
        fields = ['name', 'description', 'teams']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
