# tournaments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Tournament, BracketMatch
from .forms import TournamentForm


def tournament_list(request):
    tournaments = Tournament.objects.all().order_by('-id')
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})


@login_required
def create_tournament(request):
   
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            # save with commit=False to ensure instance saved and then save m2m if available
            t = form.save(commit=False)
            t.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return redirect('tournaments:bracket_view', pk=t.pk)
    else:
        form = TournamentForm()
    return render(request, 'tournaments/create_tournament.html', {'form': form})


def bracket_view(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    matches = BracketMatch.objects.filter(tournament=tournament).order_by('round_number')

    rounds = {}
    for m in matches:
        rounds.setdefault(m.round_number, []).append(m)

    return render(
        request,
        'tournaments/bracket.html',
        {'tournament': tournament, 'rounds': rounds}
    )


@login_required
def tournament_confirm_delete(request, pk):
    
    tournament = get_object_or_404(Tournament, pk=pk)

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete this tournament.")

    if request.method == 'POST':
        tournament.delete()
        return redirect('tournaments:tournament_list')

    return render(
        request,
        'tournaments/confirm_delete.html',
        {'object': tournament, 'type': 'Tournament'}
    )
