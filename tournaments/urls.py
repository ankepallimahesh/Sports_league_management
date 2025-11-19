# tournaments/urls.py
from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list, name='tournament_list'),
    path('create/', views.create_tournament, name='create_tournament'),
    path('<int:pk>/bracket/', views.bracket_view, name='bracket_view'),
    path('<int:pk>/delete/', views.tournament_confirm_delete, name='tournament_delete'),
]
