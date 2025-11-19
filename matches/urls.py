# matches/urls.py
from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('create/', views.create_match, name='create_match'),
    path('<int:pk>/', views.match_detail, name='match_detail'),
    path('<int:pk>/edit/', views.edit_match, name='edit_match'),
    path('<int:pk>/score/', views.record_score, name='record_score'),
    path('<int:pk>/delete/', views.match_delete, name='match_delete'),
]
