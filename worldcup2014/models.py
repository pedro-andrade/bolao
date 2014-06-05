from django.db import models
from django.core.validators import RegexValidator
            
class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.team)

class Match(models.Model):
    teamA = models.ForeignKey(Team, related_name='teamA', blank=False)
    teamB = models.ForeignKey(Team, related_name='teamB', blank=False)
    matchtime = models.DateTimeField('Date')
    winner = models.ForeignKey(Team, related_name='winner', blank=True)
    score = models.CharField(max_length=200, blank=True, validators=[RegexValidator('^((\d)|([1-9]\d*))-((\d)|([1-9]\d*))$', message='please fix score format (e.g. 0-0)', code='invalid score')])
    finish = models.BooleanField()
    
    def __unicode__(self):
        return "%s vs %s" % (self.teamA, self.teamB)

class MatchStriker(models.Model):
    match = models.ForeignKey(Match, blank=False)
    striker = models.ForeignKey(Player, blank=False)

    def __unicode__(self):
        return "%s - %s" % (self.match, self.striker)

class Vote(models.Model):
    match = models.ForeignKey(Match, blank=False)
    user = models.CharField(max_length=200, blank=False)
    striker = models.ForeignKey(Player, related_name='strikerVote', blank=False)
    winner = models.ForeignKey(Team, related_name='winnerVote', blank=False)
    score = models.CharField(max_length=200, blank=False, validators=[RegexValidator('^((\d)|([1-9]\d*))-((\d)|([1-9]\d*))$', message='please fix score format (e.g. 0-0)', code='invalid score')])
    
    def __unicode__(self):
        return "%s - %s" % (self.match, self.user)