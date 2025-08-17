from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Game, Player, Round, Score
from .forms import GameForm, RoundForm, PlayerFormSet


def home(request):
    """Home page view."""
    active_games = Game.objects.filter(is_active=True).count()
    total_games = Game.objects.count()
    total_players = Player.objects.count()
    
    context = {
        'active_games': active_games,
        'total_games': total_games,
        'total_players': total_players,
    }
    return render(request, 'score_tracker/home.html', context)


def game_list(request):
    """List all games."""
    active_games = Game.objects.filter(is_active=True).order_by('-start_date')
    completed_games = Game.objects.filter(is_active=False).order_by('-end_date')
    
    context = {
        'active_games': active_games,
        'completed_games': completed_games,
    }
    return render(request, 'score_tracker/game_list.html', context)


def game_create(request):
    """Create a new game."""
    if request.method == 'POST':
        form = GameForm(request.POST)
        player_formset = PlayerFormSet(request.POST, prefix='players')
        
        if form.is_valid() and player_formset.is_valid():
            game = form.save()
            
            # Save players
            players = []
            for player_form in player_formset:
                if player_form.is_valid() and player_form.cleaned_data.get('name'):
                    player, _ = Player.objects.get_or_create(
                        name=player_form.cleaned_data['name']
                    )
                    players.append(player)
            
            if len(players) < 3:
                messages.error(request, "You need at least 3 players for a game.")
                return render(request, 'score_tracker/game_form.html', {
                    'form': form,
                    'player_formset': player_formset,
                })
            
            game.players.set(players)
            messages.success(request, f"Game '{game.name}' created successfully!")
            return redirect('score_tracker:game_detail', pk=game.pk)
    else:
        form = GameForm()
        player_formset = PlayerFormSet(prefix='players')
    
    return render(request, 'score_tracker/game_form.html', {
        'form': form,
        'player_formset': player_formset,
    })


def game_detail(request, pk):
    """Show game details and scoreboard."""
    game = get_object_or_404(Game, pk=pk)
    rounds = game.rounds.all().order_by('round_number')
    current_scores = game.get_current_score()
    
    # Check if we have a winner
    winner = None
    max_rounds_won = 0
    for player_data in current_scores.values():
        if player_data['rounds_won'] > max_rounds_won:
            max_rounds_won = player_data['rounds_won']
            winner = player_data['player']
    
    context = {
        'game': game,
        'rounds': rounds,
        'scores': current_scores,
        'winner': winner,
        'max_rounds_won': max_rounds_won,
    }
    return render(request, 'score_tracker/game_detail.html', context)


def round_create(request, pk):
    """Create a new round for a game."""
    game = get_object_or_404(Game, pk=pk)
    
    if not game.is_active:
        messages.error(request, "Cannot add rounds to an inactive game.")
        return redirect('score_tracker:game_detail', pk=game.pk)
    
    if request.method == 'POST':
        form = RoundForm(request.POST, game=game)
        
        if form.is_valid():
            round_obj = form.save(commit=False)
            round_obj.game = game
            round_obj.round_number = game.rounds.count() + 1
            round_obj.save()
            
            # Create scores for all players except game maker
            for player in game.players.all():
                if player != round_obj.game_maker:
                    Score.objects.create(
                        round=round_obj,
                        player=player,
                        meld_points=form.cleaned_data.get(f'player_{player.id}_meld_points', 0),
                        trick_points=form.cleaned_data.get(f'player_{player.id}_trick_points', 0)
                    )
            
            messages.success(request, f"Round {round_obj.round_number} added successfully!")
            return redirect('score_tracker:game_detail', pk=game.pk)
    else:
        form = RoundForm(game=game)
    
    context = {
        'form': form,
        'game': game,
    }
    return render(request, 'score_tracker/round_form.html', context)


def end_game(request, pk):
    """End a game."""
    game = get_object_or_404(Game, pk=pk)
    
    if request.method == 'POST':
        game.end_game()
        messages.success(request, f"Game '{game.name}' has been ended.")
    
    return redirect('score_tracker:game_detail', pk=game.pk)