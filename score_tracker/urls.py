from django.urls import path
from . import views

app_name = 'score_tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('games/new/', views.game_create, name='game_create'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('games/<int:pk>/round/new/', views.round_create, name='round_create'),
    path('games/<int:pk>/end/', views.end_game, name='end_game'),
]