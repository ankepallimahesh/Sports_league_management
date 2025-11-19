from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Team, Player

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TeamRegistrationForm(forms.ModelForm):
    # allow managers to select players when creating/editing a team
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'size': 8,
            'aria-label': 'Select team players',
        })
    )

    class Meta:
        model = Team
        fields = ['name', 'short_name', 'logo', 'players']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'bio', 'photo', 'position', 'age']
