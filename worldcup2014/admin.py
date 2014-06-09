from django.contrib import admin
from worldcup2014.models import Team, Player, Match, MatchStriker, Vote, ExtraVote, Comment

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(MatchStriker)
admin.site.register(Vote)
admin.site.register(ExtraVote)
admin.site.register(Comment)


