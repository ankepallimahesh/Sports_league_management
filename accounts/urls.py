# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/choice/', views.signup_choice, name='signup_choice'),
    path('signup/manager/', views.signup_manager, name='signup_manager'),
    path('signup/player/', views.signup_player, name='signup_player'),

    path('signup/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('players/<int:pk>/', views.player_profile, name='player_profile'),
    path('players/edit/', views.edit_player, name='edit_player'),

    path('players/', views.player_list, name='player_list'),

   path('teams/', views.team_list, name='team_list'),
    path('teams/register/', views.team_register, name='team_register'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('teams/<int:pk>/edit/', views.team_edit, name='team_edit'),      # <-- ADD THIS LINE
    path('teams/<int:pk>/delete/', views.team_confirm_delete, name='team_delete'),
]
