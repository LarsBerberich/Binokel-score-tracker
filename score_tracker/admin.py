from django.contrib import admin
from .models import Player, Game, Round, Score


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('game', 'round_number', 'game_maker', 'bid_amount', 'is_success')
    list_filter = ('game', 'game_maker', 'is_success', 'is_abgehen', 'is_durch')
    inlines = [ScoreInline]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    filter_horizontal = ('players',)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'round', 'meld_points', 'trick_points', 'total_points')
    list_filter = ('player', 'round__game')