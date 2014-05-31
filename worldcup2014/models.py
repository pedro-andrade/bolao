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
    teamA = models.ForeignKey(Team, related_name='teamA')
    teamB = models.ForeignKey(Team, related_name='teamB')
    matchtime = models.DateTimeField('Date')
    striker = models.ForeignKey(Player, related_name='strikerMatch')
    winner = models.CharField(max_length=200)
    score = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s - %s " % (self.teamA, self.teamB)

class Vote(models.Model):
    matchid = models.ForeignKey(Match)
    user = models.CharField(max_length=200)
    striker = models.ForeignKey(Player, related_name='strikerVote')
    winner = models.CharField(max_length=200)
    score = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "%d - %s " % (self.matchid, self.user)    