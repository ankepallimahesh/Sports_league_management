# matches/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Goal
from .forms import ScoreForm, MatchCreateForm, GoalForm
from django.urls import reverse

def match_list(request):
    matches = Match.objects.order_by('date')
    return render(request, 'matches/match_list.html', {'matches': matches})

def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)

    form = ScoreForm(instance=match)
    goal_form = GoalForm(match=match)

    if request.method == 'POST' and 'save_score' in request.POST:
        form = ScoreForm(request.POST, instance=match)
        if form.is_valid():
            m = form.save(commit=False)
            if m.home_score is not None and m.away_score is not None:
                m.played = True
            m.save()
            return redirect('matches:match_detail', pk=match.pk)

    if request.method == 'POST' and 'add_goal' in request.POST:
        goal_form = GoalForm(request.POST, match=match)
        if goal_form.is_valid():
            g = goal_form.save(commit=False)
            g.match = match
            g.save()
            try:
                match.home_score = match.goal_set.filter(player__teams=match.home).count()
                match.away_score = match.goal_set.filter(player__teams=match.away).count()
            except Exception:
                pass
            if match.home_score is not None and match.away_score is not None:
                match.played = True
            match.save()
            return redirect('matches:match_detail', pk=match.pk)

    goals = match.goal_set.select_related('player').order_by('minute')
    return render(request, 'matches/match_detail.html', {
        'match': match,
        'form': form,
        'goal_form': goal_form,
        'goals': goals,
    })

def create_match(request):
    initial = {}
    league_id = request.GET.get('league')
    if league_id:
        initial['league'] = league_id

    if request.method == 'POST':
        form = MatchCreateForm(request.POST)
        if form.is_valid():
            m = form.save()
            return redirect('matches:match_detail', pk=m.pk)
    else:
        form = MatchCreateForm(initial=initial)

    return render(request, 'matches/create_match.html', {'form': form})

def edit_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchCreateForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('matches:match_list')
    else:
        form = MatchCreateForm(instance=match)
    return render(request, 'matches/edit_match.html', {'form': form, 'match': match})

def record_score(request, pk):
   
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=match)
        if form.is_valid():
            m = form.save(commit=False)
            if m.home_score is not None and m.away_score is not None:
                m.played = True
            m.save()
            return redirect('matches:match_detail', pk=match.pk)
    else:
        form = ScoreForm(instance=match)
    return render(request, 'matches/record_score.html', {'form': form, 'match': match})

def match_delete(request, pk):
    """
    Delete a match. You might want to protect this with a POST-only check / confirmation template.
    """
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        match.delete()
        return redirect('matches:match_list')
    return render(request, 'matches/match_confirm_delete.html', {'match': match})
