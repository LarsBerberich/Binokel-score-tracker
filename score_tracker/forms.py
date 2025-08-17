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