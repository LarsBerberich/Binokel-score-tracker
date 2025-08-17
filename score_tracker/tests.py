from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Player, Game, Round, Score
from .forms import GameForm, RoundForm


class PlayerModelTest(TestCase):
    """Test the Player model."""
    
    def setUp(self):
        self.player = Player.objects.create(name="Test Player")
    
    def test_player_creation(self):
        """Test that a player can be created."""
        self.assertEqual(self.player.name, "Test Player")
        self.assertTrue(self.player.created_at)
        self.assertTrue(self.player.updated_at)
    
    def test_player_str_representation(self):
        """Test the string representation of a player."""
        self.assertEqual(str(self.player), "Test Player")


class GameModelTest(TestCase):
    """Test the Game model."""
    
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
    
    def test_game_creation(self):
        """Test that a game can be created."""
        self.assertEqual(self.game.name, "Test Game")
        self.assertTrue(self.game.is_active)
        self.assertEqual(self.game.players.count(), 3)
        self.assertIsNone(self.game.end_date)
    
    def test_game_str_representation(self):
        """Test the string representation of a game."""
        expected = f"Test Game - {self.game.start_date.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.game), expected)
    
    def test_end_game(self):
        """Test ending a game."""
        self.assertTrue(self.game.is_active)
        self.assertIsNone(self.game.end_date)
        
        self.game.end_game()
        
        self.assertFalse(self.game.is_active)
        self.assertIsNotNone(self.game.end_date)
    
    def test_get_current_score_empty_game(self):
        """Test score calculation for a game with no rounds."""
        scores = self.game.get_current_score()
        
        self.assertEqual(len(scores), 3)
        for player_id, data in scores.items():
            self.assertEqual(data['score'], 0)
            self.assertEqual(data['rounds_won'], 0)
    
    def test_get_current_score_with_successful_round(self):
        """Test score calculation with a successful round."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=100,
            is_success=True,
            meld_points=50,
            trick_points=80
        )
        
        scores = self.game.get_current_score()
        player1_score = scores[self.player1.id]
        
        # Player 1 should have bid_amount + meld_points + trick_points
        expected_score = 100 + 50 + 80  # 230
        self.assertEqual(player1_score['score'], expected_score)
        self.assertEqual(player1_score['rounds_won'], 0)  # Not 1000 yet
    
    def test_get_current_score_with_failed_round(self):
        """Test score calculation with a failed round."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=100,
            is_success=False,
            meld_points=50,
            trick_points=80
        )
        
        scores = self.game.get_current_score()
        player1_score = scores[self.player1.id]
        
        # Player 1 should have -2*bid_amount + meld_points + trick_points
        expected_score = -2 * 100 + 50 + 80  # -70
        self.assertEqual(player1_score['score'], expected_score)
    
    def test_get_current_score_with_abgehen(self):
        """Test score calculation with abgehen."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=100,
            is_abgehen=True,
            meld_points=50,
            trick_points=80
        )
        
        scores = self.game.get_current_score()
        player1_score = scores[self.player1.id]
        
        # Player 1 should have -bid_amount + meld_points + trick_points
        expected_score = -100 + 50 + 80  # 30
        self.assertEqual(player1_score['score'], expected_score)
    
    def test_round_won_logic(self):
        """Test that a round is won when score reaches 1000."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=400,
            is_success=True,
            meld_points=300,
            trick_points=350  # Total: 400 + 300 + 350 = 1050
        )
        
        scores = self.game.get_current_score()
        player1_score = scores[self.player1.id]
        
        self.assertEqual(player1_score['rounds_won'], 1)
        self.assertEqual(player1_score['score'], 50)  # 1050 - 1000 = 50


class RoundModelTest(TestCase):
    """Test the Round model."""
    
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
    
    def test_round_creation(self):
        """Test that a round can be created."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150
        )
        
        self.assertEqual(round_obj.game, self.game)
        self.assertEqual(round_obj.round_number, 1)
        self.assertEqual(round_obj.game_maker, self.player1)
        self.assertEqual(round_obj.bid_amount, 150)
        self.assertFalse(round_obj.is_success)
        self.assertFalse(round_obj.is_abgehen)
        self.assertFalse(round_obj.is_durch)
        self.assertFalse(round_obj.is_doppelt_abgehen)
    
    def test_round_str_representation(self):
        """Test the string representation of a round."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150
        )
        expected = f"Game {self.game.id} - Round 1"
        self.assertEqual(str(round_obj), expected)
    
    def test_round_unique_constraint(self):
        """Test that round numbers are unique per game."""
        Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150
        )
        
        # This should raise an IntegrityError
        with self.assertRaises(Exception):
            Round.objects.create(
                game=self.game,
                round_number=1,  # Same round number
                game_maker=self.player2,
                bid_amount=200
            )


class DoppeltAbgehenTests(TestCase):
    """Test the new doppelt abgehen functionality."""
    
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2") 
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
    
    def test_doppelt_abgehen_field_exists(self):
        """Test that the new is_doppelt_abgehen field exists and defaults to False."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150
        )
        self.assertFalse(round_obj.is_doppelt_abgehen)
    
    def test_doppelt_abgehen_can_be_set(self):
        """Test that is_doppelt_abgehen can be set to True."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150,
            is_doppelt_abgehen=True
        )
        self.assertTrue(round_obj.is_doppelt_abgehen)
    
    def test_form_includes_doppelt_abgehen_field(self):
        """Test that RoundForm includes the new is_doppelt_abgehen field."""
        form = RoundForm(game=self.game)
        self.assertIn('is_doppelt_abgehen', form.fields)
    
    def test_doppelt_abgehen_scoring(self):
        """Test that is_doppelt_abgehen results in losing 2*bid_amount."""
        round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150,
            is_doppelt_abgehen=True,
            meld_points=50,
            trick_points=80
        )
        
        scores = self.game.get_current_score()
        # Should get -2*bid_amount + meld_points + trick_points = -300 + 50 + 80 = -170
        self.assertEqual(scores[self.player1.id]['score'], -170)
    
    def test_scoring_comparison_all_statuses(self):
        """Test scoring comparison between all four statuses."""
        bid_amount = 100
        meld_points = 30
        trick_points = 40
        
        # Test success scoring
        round_success = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=bid_amount,
            is_success=True,
            meld_points=meld_points,
            trick_points=trick_points
        )
        scores = self.game.get_current_score()
        success_score = scores[self.player1.id]['score']
        self.assertEqual(success_score, bid_amount + meld_points + trick_points)  # 170
        
        # Clear and test abgehen scoring
        self.game.rounds.all().delete()
        round_abgehen = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=bid_amount,
            is_abgehen=True,
            meld_points=meld_points,
            trick_points=trick_points
        )
        scores = self.game.get_current_score()
        abgehen_score = scores[self.player1.id]['score']
        self.assertEqual(abgehen_score, -bid_amount + meld_points + trick_points)  # -30
        
        # Clear and test doppelt abgehen scoring
        self.game.rounds.all().delete()
        round_doppelt = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=bid_amount,
            is_doppelt_abgehen=True,
            meld_points=meld_points,
            trick_points=trick_points
        )
        scores = self.game.get_current_score()
        doppelt_score = scores[self.player1.id]['score']
        self.assertEqual(doppelt_score, -2*bid_amount + meld_points + trick_points)  # -130
        
        # Verify relationships: success > abgehen > doppelt_abgehen
        self.assertGreater(success_score, abgehen_score)
        self.assertGreater(abgehen_score, doppelt_score)


class ScoreModelTest(TestCase):
    """Test the Score model."""
    
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
        self.round_obj = Round.objects.create(
            game=self.game,
            round_number=1,
            game_maker=self.player1,
            bid_amount=150
        )
    
    def test_score_creation(self):
        """Test that a score can be created."""
        score = Score.objects.create(
            round=self.round_obj,
            player=self.player2,
            meld_points=60,
            trick_points=40
        )
        
        self.assertEqual(score.round, self.round_obj)
        self.assertEqual(score.player, self.player2)
        self.assertEqual(score.meld_points, 60)
        self.assertEqual(score.trick_points, 40)
    
    def test_score_str_representation(self):
        """Test the string representation of a score."""
        score = Score.objects.create(
            round=self.round_obj,
            player=self.player2,
            meld_points=60,
            trick_points=40
        )
        expected = f"Player 2 - Round 1"
        self.assertEqual(str(score), expected)
    
    def test_total_points_property(self):
        """Test the total_points property."""
        score = Score.objects.create(
            round=self.round_obj,
            player=self.player2,
            meld_points=60,
            trick_points=40
        )
        self.assertEqual(score.total_points, 100)
    
    def test_round_points_method(self):
        """Test the round_points method for rounding logic."""
        # Test rounding down
        score = Score.objects.create(
            round=self.round_obj,
            player=self.player2,
            meld_points=63,
            trick_points=40
        )
        self.assertEqual(score.round_points(), 100)  # 103 rounds down to 100
        
        # Test rounding up
        score.meld_points = 67
        score.save()
        self.assertEqual(score.round_points(), 110)  # 107 rounds up to 110
        
        # Test exact multiple of 10
        score.meld_points = 60
        score.save()
        self.assertEqual(score.round_points(), 100)  # 100 stays 100
    
    def test_score_unique_constraint(self):
        """Test that scores are unique per round and player."""
        Score.objects.create(
            round=self.round_obj,
            player=self.player2,
            meld_points=60,
            trick_points=40
        )
        
        # This should raise an IntegrityError
        with self.assertRaises(Exception):
            Score.objects.create(
                round=self.round_obj,
                player=self.player2,  # Same player and round
                meld_points=80,
                trick_points=20
            )


class ViewTests(TestCase):
    """Test the views."""
    
    def setUp(self):
        self.client = Client()
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
    
    def test_home_view(self):
        """Test the home page view."""
        response = self.client.get(reverse('score_tracker:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Binokel Score Tracker")
        self.assertEqual(response.context['total_games'], 1)
        self.assertEqual(response.context['active_games'], 1)
        self.assertEqual(response.context['total_players'], 3)
    
    def test_game_list_view(self):
        """Test the game list view."""
        response = self.client.get(reverse('score_tracker:game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertEqual(len(response.context['active_games']), 1)
        self.assertEqual(len(response.context['completed_games']), 0)
    
    def test_game_detail_view(self):
        """Test the game detail view."""
        response = self.client.get(reverse('score_tracker:game_detail', args=[self.game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Player 1")
        self.assertContains(response, "Player 2")
        self.assertContains(response, "Player 3")
    
    def test_game_create_view_get(self):
        """Test the game create view GET request."""
        response = self.client.get(reverse('score_tracker:game_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create New Game")
    
    def test_game_create_view_post_valid(self):
        """Test the game create view POST request with valid data."""
        data = {
            'name': 'New Test Game',
            'players-TOTAL_FORMS': '3',
            'players-INITIAL_FORMS': '0',
            'players-MIN_NUM_FORMS': '3',
            'players-MAX_NUM_FORMS': '1000',
            'players-0-name': 'New Player 1',
            'players-1-name': 'New Player 2',
            'players-2-name': 'New Player 3',
        }
        
        response = self.client.post(reverse('score_tracker:game_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the game was created
        new_game = Game.objects.get(name='New Test Game')
        self.assertEqual(new_game.players.count(), 3)
    
    def test_game_create_view_post_insufficient_players(self):
        """Test the game create view POST request with insufficient players."""
        data = {
            'name': 'New Test Game',
            'players-TOTAL_FORMS': '2',
            'players-INITIAL_FORMS': '0',
            'players-MIN_NUM_FORMS': '3',
            'players-MAX_NUM_FORMS': '1000',
            'players-0-name': 'New Player 1',
            'players-1-name': 'New Player 2',
        }
        
        response = self.client.post(reverse('score_tracker:game_create'), data)
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertContains(response, "You need at least 3 players")
    
    def test_round_create_view_get(self):
        """Test the round create view GET request."""
        response = self.client.get(reverse('score_tracker:round_create', args=[self.game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Add Round for {self.game.name}")
    
    def test_round_create_view_post_valid(self):
        """Test the round create view POST request with valid data."""
        data = {
            'game_maker': self.player1.pk,
            'bid_amount': 150,
            'is_success': True,
            'meld_points': 60,
            'trick_points': 80,
            f'player_{self.player2.id}_meld_points': 40,
            f'player_{self.player2.id}_trick_points': 50,
            f'player_{self.player3.id}_meld_points': 30,
            f'player_{self.player3.id}_trick_points': 60,
        }
        
        response = self.client.post(reverse('score_tracker:round_create', args=[self.game.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the round was created
        round_obj = Round.objects.get(game=self.game, round_number=1)
        self.assertEqual(round_obj.game_maker, self.player1)
        self.assertEqual(round_obj.bid_amount, 150)
        self.assertTrue(round_obj.is_success)
        
        # Check that scores were created for other players
        self.assertEqual(Score.objects.filter(round=round_obj).count(), 2)
    
    def test_round_create_view_inactive_game(self):
        """Test that rounds cannot be added to inactive games."""
        self.game.end_game()
        response = self.client.get(reverse('score_tracker:round_create', args=[self.game.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to game detail
    
    def test_end_game_view(self):
        """Test the end game view."""
        self.assertTrue(self.game.is_active)
        
        response = self.client.post(reverse('score_tracker:end_game', args=[self.game.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to game detail
        
        # Check that the game was ended
        self.game.refresh_from_db()
        self.assertFalse(self.game.is_active)
        self.assertIsNotNone(self.game.end_date)


class FormTests(TestCase):
    """Test the forms."""
    
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.game = Game.objects.create(name="Test Game")
        self.game.players.set([self.player1, self.player2, self.player3])
    
    def test_game_form_valid(self):
        """Test GameForm with valid data."""
        form_data = {'name': 'Test Game'}
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_game_form_invalid(self):
        """Test GameForm with invalid data."""
        form_data = {'name': ''}  # Name is required
        form = GameForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_round_form_valid(self):
        """Test RoundForm with valid data."""
        form_data = {
            'game_maker': self.player1.pk,
            'bid_amount': 150,
            'is_success': True,
            'meld_points': 60,
            'trick_points': 80,
        }
        form = RoundForm(data=form_data, game=self.game)
        self.assertTrue(form.is_valid())
    
    def test_round_form_invalid_bid(self):
        """Test RoundForm with invalid bid amount."""
        form_data = {
            'game_maker': self.player1.pk,
            'bid_amount': 0,  # Must be at least 1
            'is_success': True,
            'meld_points': 60,
            'trick_points': 80,
        }
        form = RoundForm(data=form_data, game=self.game)
        self.assertFalse(form.is_valid())
    
    def test_round_form_player_queryset(self):
        """Test that RoundForm limits players to game players."""
        other_player = Player.objects.create(name="Other Player")
        form = RoundForm(game=self.game)
        
        # Check that only game players are in the queryset
        game_maker_choices = form.fields['game_maker'].queryset
        self.assertIn(self.player1, game_maker_choices)
        self.assertIn(self.player2, game_maker_choices)
        self.assertIn(self.player3, game_maker_choices)
        self.assertNotIn(other_player, game_maker_choices)
    
    def test_round_form_dynamic_fields(self):
        """Test that RoundForm creates dynamic fields for each player."""
        form = RoundForm(game=self.game)
        
        # Check that fields are created for each player
        self.assertIn(f'player_{self.player1.id}_meld_points', form.fields)
        self.assertIn(f'player_{self.player1.id}_trick_points', form.fields)
        self.assertIn(f'player_{self.player2.id}_meld_points', form.fields)
        self.assertIn(f'player_{self.player2.id}_trick_points', form.fields)
        self.assertIn(f'player_{self.player3.id}_meld_points', form.fields)
        self.assertIn(f'player_{self.player3.id}_trick_points', form.fields)


class IntegrationTests(TestCase):
    """Integration tests for complete game workflows."""
    
    def test_complete_game_workflow(self):
        """Test a complete game from creation to completion."""
        # Create players
        player1 = Player.objects.create(name="Alice")
        player2 = Player.objects.create(name="Bob")
        player3 = Player.objects.create(name="Charlie")
        
        # Create game
        game = Game.objects.create(name="Integration Test Game")
        game.players.set([player1, player2, player3])
        
        # Add first round - successful
        round1 = Round.objects.create(
            game=game,
            round_number=1,
            game_maker=player1,
            bid_amount=200,
            is_success=True,
            meld_points=100,
            trick_points=150
        )
        
        # Add scores for other players
        Score.objects.create(round=round1, player=player2, meld_points=50, trick_points=60)
        Score.objects.create(round=round1, player=player3, meld_points=40, trick_points=70)
        
        # Check scores after round 1
        scores = game.get_current_score()
        self.assertEqual(scores[player1.id]['score'], 450)  # 200 + 100 + 150
        self.assertEqual(scores[player2.id]['score'], 110)  # 50 + 60
        self.assertEqual(scores[player3.id]['score'], 110)  # 40 + 70
        
        # Add second round - failed
        round2 = Round.objects.create(
            game=game,
            round_number=2,
            game_maker=player2,
            bid_amount=300,
            is_success=False,
            meld_points=80,
            trick_points=90
        )
        
        Score.objects.create(round=round2, player=player1, meld_points=60, trick_points=80)
        Score.objects.create(round=round2, player=player3, meld_points=70, trick_points=75)
        
        # Check scores after round 2
        scores = game.get_current_score()
        self.assertEqual(scores[player1.id]['score'], 590)  # 450 + 60 + 80
        self.assertEqual(scores[player2.id]['score'], -320)  # 110 - 600 + 80 + 90 = 110 - 600 + 170 = -320
        self.assertEqual(scores[player3.id]['score'], 255)  # 110 + 70 + 75
        
        # Add third round that makes player1 win a round
        round3 = Round.objects.create(
            game=game,
            round_number=3,
            game_maker=player1,
            bid_amount=400,
            is_success=True,
            meld_points=200,
            trick_points=300
        )
        
        # Check scores - player1 should win one round
        scores = game.get_current_score()
        self.assertEqual(scores[player1.id]['rounds_won'], 1)
        self.assertEqual(scores[player1.id]['score'], 490)  # (590 + 900) - 1000 = 490
        
        # End the game
        game.end_game()
        self.assertFalse(game.is_active)
        self.assertIsNotNone(game.end_date)
