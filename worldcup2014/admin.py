from django.contrib import admin
from worldcup2014.models import Team, Player, Match, MatchStriker, Vote

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(MatchStriker)
admin.site.register(Vote)


