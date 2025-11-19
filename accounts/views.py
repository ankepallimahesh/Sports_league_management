# accounts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import models as djmodels

from .forms import SignUpForm, TeamRegistrationForm, PlayerForm


from .models import Player, Team

def signup_choice(request):
   
    return render(request, 'accounts/signup_choice.html')


def signup_manager(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        team_form = TeamRegistrationForm(request.POST, request.FILES)
        if form.is_valid() and team_form.is_valid():
            user = form.save()
            try:
                Player.objects.create(user=user, full_name=user.username)
            except Exception:
                pass
            login(request, user)
            try:
                team = team_form.save()
                try:
                    player = user.player
                    team.players.add(player)
                except Exception:
                    pass
            except Exception:
                pass
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()
        team_form = TeamRegistrationForm()
    return render(request, 'accounts/signup_manager.html', {
        'form': form,
        'team_form': team_form,
    })


def signup_player(request):
   
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        player_form = PlayerForm(request.POST, request.FILES)
        if form.is_valid() and player_form.is_valid():
            user = form.save()
            login(request, user)
            player = player_form.save(commit=False)
            player.user = user
            player.save()
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()
        player_form = PlayerForm()
    return render(request, 'accounts/signup_player.html', {
        'form': form,
        'player_form': player_form,
    })


def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = getattr(form, 'cleaned_data', {}).get('full_name') or user.username
            try:
                Player.objects.create(user=user, full_name=full_name)
            except Exception:
                pass
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# accounts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import TeamRegistrationForm

@login_required
def team_edit(request, pk):
   
    team = get_object_or_404(Team, pk=pk)
    user_is_member = request.user.is_staff or (hasattr(request.user, 'player') and team.players.filter(user=request.user).exists())
    if not user_is_member:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to edit this team.")

    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('accounts:team_detail', pk=team.pk)
    else:
        form = TeamRegistrationForm(instance=team)

    return render(request, 'teams/team_edit.html', {'form': form, 'team': team})


@login_required
def dashboard(request):
    """
    Simple dashboard: managers (users whose player is in teams) see manager dashboard,
    others see player dashboard.
    """
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        player = None

    teams = Team.objects.filter(players__user=request.user).distinct()

    if teams.exists():
        return render(request, 'accounts/dashboard_manager.html', {'teams': teams})
    else:
        return render(request, 'accounts/dashboard_player.html', {'player': player})

@login_required
def edit_player(request):
    player, created = Player.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect('accounts:player_profile', pk=player.pk)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'accounts/edit_player.html', {'form': form})


def player_profile(request, pk):
    """
    Public player profile with computed statistics.
    """
    player = get_object_or_404(Player, pk=pk)

    try:
        from matches.models import Goal, Match
    except Exception:
        Goal = None
        Match = None

    goals = Goal.objects.filter(player=player).count() if Goal else 0

    teams = player.teams.all()
    matches_played = 0
    wins = losses = draws = 0

    if Match:
        qs = Match.objects.filter(djmodels.Q(home__in=teams) | djmodels.Q(away__in=teams), played=True).distinct()
        matches_played = qs.count()
        for m in qs:
            winner = m.winner()
            if winner is None:
                draws += 1
            elif winner in teams:
                wins += 1
            else:
                losses += 1

    # Determine whether the current request user can edit this profile (owner or staff)
    try:
        can_edit = request.user.is_authenticated and (request.user.is_staff or request.user == player.user)
    except Exception:
        can_edit = False

    return render(request, 'accounts/player_profile.html', {
        'player': player,
        'goals': goals,
        'matches_played': matches_played,
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'can_edit': can_edit,
    })



def team_list(request):
    teams = list(Team.objects.all())
    # annotate each team with whether the current user is a manager/member for template use
    for team in teams:
        try:
            user_is_member = request.user.is_staff or (hasattr(request.user, 'player') and team.players.filter(user=request.user).exists())
        except Exception:
            user_is_member = False
        team.user_is_member = user_is_member
    return render(request, 'teams/team_list.html', {'teams': teams})


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    try:
        user_is_member = request.user.is_staff or (hasattr(request.user, 'player') and team.players.filter(user=request.user).exists())
    except Exception:
        user_is_member = False
    team.user_is_member = user_is_member
    return render(request, 'teams/team_detail.html', {'team': team})


@login_required
def team_confirm_delete(request, pk):
    """
    Confirm (GET) and perform (POST) delete for a Team.
    Permission: user must be team member or staff.
    """
    team = get_object_or_404(Team, pk=pk)
    user_is_member = request.user.is_staff or (hasattr(request.user, 'player') and team.players.filter(user=request.user).exists())
    if not user_is_member:
        return HttpResponseForbidden("You don't have permission to delete this team.")
    if request.method == 'POST':
        team.delete()
        # use the namespaced URL name from accounts.urls
        return redirect('accounts:team_list')
    return render(request, 'teams/confirm_delete.html', {'object': team, 'type': 'Team'})


@login_required
def team_register(request):
    """
    Register / create a new team.
    After successful creation redirect to accounts:team_detail (namespaced).
    """
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()
            return redirect('accounts:team_detail', pk=team.pk)
    else:
        form = TeamRegistrationForm()
    return render(request, 'accounts/team_register.html', {'form': form})


def player_list(request):
    players = list(Player.objects.all())
    # Attach recent matches played (up to 5) for each player to avoid complex template logic
    try:
        from matches.models import Match, Goal
        from django.db.models import Q
        for p in players:
            # include matches where player's team was home/away OR the player scored in the match
            qs = (
                Match.objects
                .filter(Q(home__players=p) | Q(away__players=p) | Q(goal__player=p))
                .select_related('home', 'away')
                .prefetch_related('home__players', 'away__players')
                .distinct()
                .order_by('-date')[:5]
            )
            recent = []
            for m in qs:
                # determine which team(s) the player belongs to in this match (if any)
                played_for = None
                opponent = None
                side = None
                try:
                    if p in m.home.players.all():
                        played_for = m.home
                        opponent = m.away
                        side = 'home'
                    elif p in m.away.players.all():
                        played_for = m.away
                        opponent = m.home
                        side = 'away'
                except Exception:
                    # if players relation not accessible for some reason, leave as None
                    pass
                recent.append({'match': m, 'team': played_for, 'opponent': opponent, 'side': side})
            p.recent_matches = recent
    except Exception:
        # If matches app is not available for any reason, just continue without recent matches
        for p in players:
            p.recent_matches = []

    return render(request, 'players/player_list.html', {'players': players})
