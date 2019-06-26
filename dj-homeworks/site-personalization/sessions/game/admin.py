from django.contrib import admin
from .models import Player, Game, PlayerGameInfo


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_main')
    

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'counts', 'status')
    list_display_links = ('id', 'number', 'counts', 'status')
    
    
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
