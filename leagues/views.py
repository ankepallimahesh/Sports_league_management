# leagues/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import League
from .forms import LeagueForm
from django.shortcuts import get_object_or_404, redirect

def add_teams_to_league(request, pk):
    
    league = get_object_or_404(League, pk=pk)
    team_id = request.GET.get('team')
    if team_id:
        try:
            from accounts.models import Team as TeamModel
            team = TeamModel.objects.get(pk=team_id)
            league.teams.add(team)
        except TeamModel.DoesNotExist:
            pass
    return redirect('league_detail', pk=pk)
def league_list(request):
    """
    Show all leagues.
    """
    leagues = League.objects.all().order_by('name')
    return render(request, 'leagues/league_list.html', {'leagues': leagues})

def league_detail(request, pk):
   
    league = get_object_or_404(League, pk=pk)
    teams = league.teams.all()
    try:
        from matches.models import Match
        matches = Match.objects.filter(league=league).order_by('date')
    except Exception:
        matches = []
    return render(request, 'leagues/league_detail.html', {
        'league': league,
        'teams': teams,
        'matches': matches,
    })

def create_league(request):
    
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        if form.is_valid():
            # use commit=False to ensure we have the instance saved explicitly,
            # then save m2m if available. Also redirect to the namespaced URL.
            league = form.save(commit=False)
            league.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return redirect('leagues:league_detail', pk=league.pk)
    else:
        form = LeagueForm()
    return render(request, 'leagues/create_league.html', {'form': form})

def add_teams_to_league(request, pk):
    
    league = get_object_or_404(League, pk=pk)
    team_id = request.GET.get('team')
    if team_id:
        try:
            from accounts.models import Team as TeamModel
            team = TeamModel.objects.get(pk=team_id)
            league.teams.add(team)
        except TeamModel.DoesNotExist:
            pass
    return redirect('leagues:league_detail', pk=pk)

def standings(request, pk):
    """
    Compute and display standings for the league:
    points (3/1/0), played, won, draw, lost, goals for/against, goal diff.
    """
    league = get_object_or_404(League, pk=pk)
    teams = list(league.teams.all())

    table = {
        t.id: {
            'team': t, 'played': 0, 'won': 0, 'draw': 0, 'lost': 0,
            'gf': 0, 'ga': 0, 'gd': 0, 'points': 0
        } for t in teams
    }

    try:
        from matches.models import Match
    except Exception:
        Match = None

    if Match:
        matches = Match.objects.filter(league=league, played=True)
        for m in matches:
            home = m.home
            away = m.away
            hs = m.home_score or 0
            as_ = m.away_score or 0

            table[home.id]['played'] += 1
            table[away.id]['played'] += 1

            table[home.id]['gf'] += hs
            table[home.id]['ga'] += as_
            table[away.id]['gf'] += as_
            table[away.id]['ga'] += hs

            if hs > as_:
                table[home.id]['won'] += 1
                table[away.id]['lost'] += 1
                table[home.id]['points'] += 3
            elif hs < as_:
                table[away.id]['won'] += 1
                table[home.id]['lost'] += 1
                table[away.id]['points'] += 3
            else:
                table[home.id]['draw'] += 1
                table[away.id]['draw'] += 1
                table[home.id]['points'] += 1
                table[away.id]['points'] += 1

    for v in table.values():
        v['gd'] = v['gf'] - v['ga']

    standings_list = sorted(
        table.values(),
        key=lambda x: (-x['points'], -x['gd'], -x['gf'])
    )

    return render(request, 'leagues/standings.html', {
        'league': league,
        'standings': standings_list,
    })

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def league_confirm_delete(request, pk):
    league = get_object_or_404(League, pk=pk)
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete this league.")
    if request.method == 'POST':
        league.delete()
    return redirect('leagues:league_list')
    return render(request, 'leagues/confirm_delete.html', {'object': league, 'type': 'League'})
