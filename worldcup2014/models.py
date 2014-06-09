from django.db import models
from django.core.validators import RegexValidator
            
class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    group = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
    
class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)
    
    def __unicode__(self):
        return "[%s] %s" % (self.team, self.name)
    
class Match(models.Model):
    teamA = models.ForeignKey(Team, related_name='teamA', blank=False)
    teamB = models.ForeignKey(Team, related_name='teamB', blank=False)
    matchtime = models.DateTimeField('Date')
    winner = models.ForeignKey(Team, related_name='winner', blank=True)
    score = models.CharField(max_length=200, blank=True, validators=[RegexValidator('^((\d)|([1-9]\d*))-((\d)|([1-9]\d*))$', message='please fix score format (e.g. 0-0)', code='invalid score')])
    finish = models.BooleanField()
    stage = models.CharField(max_length=200)
    #   strikers = models.ManyToManyField(Player, null=True, blank=True)
    
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
    
class ExtraVote(models.Model):
    user = models.CharField(max_length=200, blank=False)
    striker = models.ForeignKey(Player, related_name='strikerExtraVote', blank=False)
    winner = models.ForeignKey(Team, related_name='winnerExtraVote', blank=False)
    
    def __unicode__(self):
        return "%s" % (self.user)
    
class Comment(models.Model):
    user = models.CharField(max_length=200, blank=False)
    comment = models.CharField(max_length=2000, blank=False)
    
    def __unicode__(self):
        return "%s - %s" % (self.user, self.comment)
        