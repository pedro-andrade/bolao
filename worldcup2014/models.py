from django.db import models
            
class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return self.name
        
class Match(models.Model):
    teamA = models.ForeignKey(Team, related_name='teamA', blank=False)
    teamB = models.ForeignKey(Team, related_name='teamB', blank=False)
    matchtime = models.DateTimeField('Date')
    winner = models.ForeignKey(Team, related_name='winner', blank=True)
    score = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return "%s - %s " % (self.teamA, self.teamB)

class MatchStriker(models.Model):
    match = models.ForeignKey(Match, blank=False)
    striker = models.ForeignKey(Player, blank=False)
    
    def __unicode__(self):
        return "%d - %d " % (self.match, self.striker)

class Vote(models.Model):
    match = models.ForeignKey(Match)
    user = models.CharField(max_length=200, blank=False)
    striker = models.ForeignKey(Player, related_name='strikerVote', blank=False)
    winner = models.ForeignKey(Team, related_name='winnerVote', blank=False)
    score = models.CharField(max_length=200, blank=False)
    
    def __unicode__(self):
        return "%s - %s " % (self.match, self.user)