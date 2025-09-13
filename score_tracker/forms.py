from django import forms
from django.forms import inlineformset_factory
from .models import Game, Round, Player, Score


class GameForm(forms.ModelForm):
    """Form for creating a new game."""
    class Meta:
        model = Game
        fields = ['name']


class PlayerForm(forms.ModelForm):
    """Form for creating a new player."""
    class Meta:
        model = Player
        fields = ['name']


PlayerFormSet = inlineformset_factory(
    Game, 
    Game.players.through, 
    fields=('player',),
    extra=3,
    min_num=3,
    validate_min=True,
    can_delete=False,
)

# Create a custom formset for player creation
PlayerFormSet = forms.formset_factory(
    form=PlayerForm,
    extra=3,
    min_num=3,
    validate_min=True,
)


class RoundForm(forms.ModelForm):
    """Form for creating a new round."""
    class Meta:
        model = Round
        fields = [
            'game_maker', 'bid_amount', 'is_success', 'is_abgehen', 'is_durch', 'is_doppelt_abgehen',
            'meld_points', 'trick_points', 'last_trick_winner'
        ]
        widgets = {
            'is_success': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_abgehen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_durch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_doppelt_abgehen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        
        if self.game:
            # Limit player choices to players in this game
            players = self.game.players.all()
            self.fields['game_maker'].queryset = players
            self.fields['last_trick_winner'].queryset = players
            
            # Add fields for each player's meld points and trick points
            for player in players:
                self.fields[f'player_{player.id}_meld_points'] = forms.IntegerField(
                    label=f"{player.name}'s meld points",
                    required=False,
                    min_value=0,
                    initial=0,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )
                self.fields[f'player_{player.id}_trick_points'] = forms.IntegerField(
                    label=f"{player.name}'s trick points",
                    required=False,
                    min_value=0,
                    initial=0,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )

    def clean(self):
        """Custom validation for the entire form."""
        cleaned_data = super().clean()
        
        if not self.game:
            return cleaned_data
        
        # Validate total trick points don't exceed 250
        total_trick_points = 0
        game_maker_id = cleaned_data.get('game_maker')
        
        # Add game maker's trick points
        game_maker_trick_points = cleaned_data.get('trick_points', 0) or 0
        total_trick_points += game_maker_trick_points
        
        # Add other players' trick points (excluding game maker)
        for player in self.game.players.all():
            if game_maker_id and player.id != game_maker_id.id:
                player_trick_points = cleaned_data.get(f'player_{player.id}_trick_points', 0) or 0
                total_trick_points += player_trick_points
        
        if total_trick_points > 250:
            raise forms.ValidationError(
                f"Total trick points ({total_trick_points}) cannot exceed 250. "
                f"In Binokel, there are exactly 250 trick points per round."
            )
        
        return cleaned_data