# leagues/urls.py
from django.urls import path
from . import views
app_name='leagues'
urlpatterns = [
    path('', views.league_list, name='league_list'),
    path('create/', views.create_league, name='create_league'),
    path('<int:pk>/', views.league_detail, name='league_detail'),
    path('<int:pk>/standings/', views.standings, name='standings'),
    path('<int:pk>/add_team/', getattr(views, 'add_teams_to_league', views.league_detail), name='add_team_to_league'),
    path('<int:pk>/remove_team/<int:team_pk>/', getattr(views, 'remove_team_from_league', views.league_detail), name='remove_team_from_league'),
    path('<int:pk>/delete/', getattr(views, 'league_confirm_delete', views.league_detail), name='league_delete'),
]
