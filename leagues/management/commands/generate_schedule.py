from django.core.management.base import BaseCommand
from leagues.models import League
from matches.models import Match

class Command(BaseCommand):
    help = 'Generate a round-robin schedule for a league (creates Match objects)'

    def add_arguments(self, parser):
        parser.add_argument('league_id', type=int)

    def handle(self, *args, **options):
        league_id = options['league_id']
        try:
            league = League.objects.get(pk=league_id)
        except League.DoesNotExist:
            self.stdout.write(self.style.ERROR('League not found'))
            return

        teams = list(league.teams.all())
        if len(teams) < 2:
            self.stdout.write(self.style.ERROR('Need at least 2 teams to generate schedule'))
            return

        # round robin algorithm (simple)
        if len(teams) % 2 == 1:
            teams.append(None)

        n = len(teams)
        rounds = n - 1
        half = n // 2

        Match.objects.filter(league=league).delete()  # clear existing
        for r in range(rounds):
            for i in range(half):
                t1 = teams[i]
                t2 = teams[n - 1 - i]
                if t1 is None or t2 is None:
                    continue
                Match.objects.create(league=league, home=t1, away=t2)
            teams.insert(1, teams.pop())
        self.stdout.write(self.style.SUCCESS('Schedule generated'))
