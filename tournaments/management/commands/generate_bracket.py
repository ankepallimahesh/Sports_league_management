# tournaments/management/commands/generate_bracket.py
from django.core.management.base import BaseCommand
from tournaments.models import Tournament, BracketMatch
import math

class Command(BaseCommand):
    help = 'Generate single-elimination bracket for a tournament (fills BracketMatch)'

    def add_arguments(self, parser):
        parser.add_argument('tournament_id', type=int)

    def handle(self, *args, **options):
        tid = options['tournament_id']
        try:
            t = Tournament.objects.get(pk=tid)
        except Tournament.DoesNotExist:
            self.stdout.write(self.style.ERROR('Tournament not found'))
            return

        teams = list(t.teams.all())
        if len(teams) < 2:
            self.stdout.write(self.style.ERROR('Need at least 2 teams'))
            return

        # clear existing bracket matches
        BracketMatch.objects.filter(tournament=t).delete()

        # Next power of two
        n = len(teams)
        rounds = math.ceil(math.log2(n))
        total_slots = 2 ** rounds
        # add byes as None
        slots = teams + [None] * (total_slots - n)

        # first round pairings
        matches = []
        round_num = 1
        for i in range(total_slots // 2):
            home = slots[i]
            away = slots[total_slots - 1 - i]
            if home is None or away is None:
                # if one is None, the other advances automatically (no BracketMatch created now)
                if home is None and away is None:
                    continue
            if home and away:
                bm = BracketMatch.objects.create(tournament=t, round_number=round_num, home=home, away=away)
                matches.append(bm)

        self.stdout.write(self.style.SUCCESS(f'Created {len(matches)} matches in round 1 for tournament {t.name}'))
