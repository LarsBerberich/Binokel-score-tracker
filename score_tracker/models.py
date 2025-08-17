from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Player(models.Model):
    """Player model to store player information."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    """Game model to store game information."""
    name = models.CharField(max_length=100, default="Binokel Game")
    players = models.ManyToManyField(Player, related_name='games')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.start_date.strftime('%Y-%m-%d %H:%M')}"

    def end_game(self):
        """End the game."""
        self.is_active = False
        self.end_date = timezone.now()
        self.save()

    def get_current_score(self):
        """Calculate the current score for each player."""
        result = {}
        for player in self.players.all():
            score = 0
            rounds_won = 0
            
            # Process all rounds chronologically
            all_rounds = self.rounds.all().order_by('round_number')
            
            for round_obj in all_rounds:
                round_score = 0
                
                if round_obj.game_maker == player:
                    # Game maker scoring
                    if round_obj.is_success:
                        round_score += round_obj.bid_amount
                    elif round_obj.is_abgehen:
                        round_score -= round_obj.bid_amount
                    elif round_obj.is_doppelt_abgehen:
                        round_score -= 2 * round_obj.bid_amount
                    else:
                        # Default case: if none of the above are set, it's considered a failed attempt (doppelt abgehen)
                        round_score -= 2 * round_obj.bid_amount
                    # Note: is_durch doesn't affect scoring differently, it's just a flag
                    
                    # Add meld points and trick points
                    round_score += round_obj.meld_points + round_obj.trick_points
                else:
                    # Other player scoring - only meld and trick points
                    player_score = Score.objects.filter(round=round_obj, player=player).first()
                    if player_score:
                        round_score += player_score.meld_points + player_score.trick_points
                
                # Add round score to total
                score += round_score
                
                # Check if round is won after this round
                while score >= 1000:
                    rounds_won += 1
                    score -= 1000
            
            result[player.id] = {
                'player': player,
                'score': score,
                'rounds_won': rounds_won
            }
        
        return result


class Round(models.Model):
    """Round model to store information about each round of the game."""
    game = models.ForeignKey(Game, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.PositiveIntegerField()
    game_maker = models.ForeignKey(Player, related_name='rounds_as_game_maker', on_delete=models.CASCADE)
    bid_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_success = models.BooleanField(default=False)
    is_abgehen = models.BooleanField(default=False)  # If game maker chooses to "go down"
    is_durch = models.BooleanField(default=False)    # If game maker attempts a "Durch"
    is_doppelt_abgehen = models.BooleanField(default=False)  # If game maker fails to reach bid amount
    meld_points = models.PositiveIntegerField(default=0)  # Meld points for the game maker
    trick_points = models.PositiveIntegerField(default=0)  # Trick points for the game maker
    last_trick_winner = models.ForeignKey(
        Player, 
        related_name='rounds_with_last_trick', 
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['game', 'round_number']
        ordering = ['game', 'round_number']

    def __str__(self):
        return f"Game {self.game.id} - Round {self.round_number}"


class Score(models.Model):
    """Score model to store the score of each player in a round."""
    round = models.ForeignKey(Round, related_name='scores', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    meld_points = models.PositiveIntegerField(default=0)  # Meld points
    trick_points = models.PositiveIntegerField(default=0)  # Trick points
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['round', 'player']

    def __str__(self):
        return f"{self.player.name} - Round {self.round.round_number}"

    @property
    def total_points(self):
        """Calculate total points for this score."""
        return self.meld_points + self.trick_points

    def round_points(self):
        """Round points according to the rules."""
        points = self.total_points
        remainder = points % 10
        
        if remainder >= 5:
            return points + (10 - remainder)  # Round up
        else:
            return points - remainder  # Round down